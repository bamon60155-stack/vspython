from langchain_core.tools import tool
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from clean_low_quality_chunk import is_low_quality_chunk
from vector_store import vector_store

# 只在模块加载的时候执行一次的准备工作

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ",""]
)

paper_files = [
    "starlink_paper.txt",
    "fisher_info_paper.txt",
    "pa_feature_paper.txt"
]

all_chunks = []
for file_path in paper_files:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = splitter.split_text(text)
    good_chunks = [c for c in chunks if not is_low_quality_chunk(c)]
    all_chunks.extend(good_chunks)

collection = vector_store(all_chunks, collection_name="rffi_papers")

# 论文table I的星座矩两=量数据(写死成一个查找表)
CONSTELLATION_PARAMS = {
    "BPSK":   {"mu20": 1.0, "beta": 0,    "mu4": 1.0,  "mu6": 1.0},
    "QPSK":   {"mu20": 0.0, "beta": 1,    "mu4": 1.0,  "mu6": 1.0},
    "8PSK":   {"mu20": 0.0, "beta": 1,    "mu4": 1.0,  "mu6": 1.0},
    "16QAM":  {"mu20": 0.0, "beta": 1,    "mu4": 1.32, "mu6": 1.96},
    "64QAM":  {"mu20": 0.0, "beta": 1,    "mu4": 1.38, "mu6": 2.23},
}

# 工具定义
@tool
def search_document(query: str) -> str:
     """搜索卫星通信与RF指纹识别(RFFI)领域的专业文献知识库，
    涵盖内容包括:Starlink Ku波段下行信号结构与仿真、卫星RF指纹身份识别的
    Fisher信息量与可辨识性理论、功放(PA)非线性特征的深度学习建模方法。
    当用户询问卫星通信协议、信号结构、Doppler补偿、IQ不平衡、功放非线性、
    RF指纹识别、Iridium/Starlink相关技术问题时使用。
    输入用户的问题，返回相关的论文原文片段。"""
     results = collection.query(query_texts=[query], n_results=4)
     retrived_chunks = results["documents"][0]
     return "\n\n".join(retrived_chunks)

@tool
def get_current_time() -> str:
    """获取当前的日期和时间"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate_crb(constellation: str, N: int, snr_db: float) -> str:
    """根据调制星座类型、已知符号数N、信噪比(dB)，计算RF指纹识别中
    IQ不平衡参数ε和PA非线性参数Re(alpha3)的Cramer-Rao下界(CRB)，
    并判断该调制方式下IQ不平衡参数是否可辨识(identifiable)。
    支持的星座类型：BPSK, QPSK, 8PSK, 16QAM, 64QAM
    当用户询问某种调制方式下的CRB、可辨识性、Fisher信息量相关计算时使用。"""

    constellation = constellation.upper().replace("-", "")
    if constellation not in CONSTELLATION_PARAMS:
        return f"不支持的调制类型：{constellation}，支持的类型有：{list(CONSTELLATION_PARAMS.keys())}"
    
    params = CONSTELLATION_PARAMS[constellation]
    beta = params["beta"]
    mu6 = params["mu6"]
    
    gamma = 10 ** (snr_db / 10)   # dB转线性SNR
    
    if beta == 0:
        crb_eps = float("inf")
        identifiable = "不可辨识（β=0，FIM秩亏，无法通过任何无偏估计器恢复IQ参数）"
    else:
        crb_eps = 1 / (N * gamma)   # 正比例关系，简化系数为1
        identifiable = "可辨识（β=1，IQ参数与PA参数均可独立估计）"
    
    crb_alpha3 = 1 / (N * gamma * mu6)
    
    result = f"""调制方式：{constellation}
         可辨识性因子 β = {beta}
         IQ不平衡参数可辨识性：{identifiable}
         CRB(ε) ≈ {crb_eps if crb_eps == float('inf') else f'{crb_eps:.6e}'}
         CRB(Re(α3)) ≈ {crb_alpha3:.6e}
         （μ6 = {mu6}，N = {N}，SNR = {snr_db} dB）"""
    
    return result

# 接入Agent，测试
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import os

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

tools = [get_current_time, search_document, calculate_crb]
agent = create_agent(llm, tools)

response = agent.invoke({"messages":[{"role": "user", "content": "帮我算一下BPSK调制、已知符号数76、信噪比20dB情况下的CRB"}]})
print(response["messages"][-1].content)
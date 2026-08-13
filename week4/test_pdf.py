import pdfplumber
from clean_pdf_text import clean_pdf_text,clean_pdf_text_two_column
from document_loader import split_by_paragraph, split_text
from clean_low_quality_chunk import is_low_quality_chunk
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n","\n", ".", " ",""]

)


cleaned1 = clean_pdf_text("week4/komodromos_starlink_simulator.pdf")
with open("week4/starlink_paper.txt", "w", encoding="utf-8") as f:
    f.write(cleaned1)

cleaned2 = clean_pdf_text_two_column("week4/2603.29766v1.pdf")
with open("week4/fisher_info_paper.txt", "w", encoding="utf-8") as f:
    f.write(cleaned2)


cleaned3 = clean_pdf_text("week4/[C]2025_INFOCOM_WS_An_Investigation_of_Power_Amplifier_Feature_for_Deep_Learning_Based_RF_Fingerprint_Identification.pdf")
with open("week4/pa_feature_paper.txt", "w", encoding="utf-8") as f:
    f.write(cleaned3)

# 用一篇文献来试验一下
with open("week4/fisher_info_paper.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = splitter.split_text(text)

good_chunks = [c for c in chunks if not is_low_quality_chunk(c)]

print(f"切分出{len(chunks)}块，过滤后剩下{len(good_chunks)}块")
print(f"被过滤掉了{len(chunks) - len(good_chunks)}块")

# 抽查几个被过滤掉的块，确认过滤器判断的对不对
bad_chunks = [c for c in chunks if is_low_quality_chunk(c)]
for c in bad_chunks[:3]:
    print("---被过滤的块---")
    print(c[:100])

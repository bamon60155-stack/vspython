import re
import pdfplumber

def clean_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
            if page_text:
                all_text.append(page_text)

    full_text = "\n".join(all_text)

    # 去掉常见的页眉模式（比如期刊名+页码这种反复出现的行）
    full_text = re.sub(r'IEEE TRANSACTIONS ON.*\n', '', full_text)
    full_text = re.sub(r'^\d+\s*$', '', full_text, flags=re.MULTILINE)# 单独一行只有数字的（页码）

    return full_text

def clean_pdf_text_two_column(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        for page in pdf.pages:
            width = page.width
            height = page.height

            # 左栏：页面左半边
            left = page.crop((0, 0 , width/2, height))
            # 右栏：页面右半边
            right = page.crop((width/2, 0, width, height))

            left_text = left.extract_text(x_tolerance=1, y_tolerance=1)
            right_text = right.extract_text(x_tolerance=1, y_tolerance=1)

            if left_text:
                all_text.append(left_text)
            if right_text:
                all_text.append(right_text)

    full_text = "\n".join(all_text)
    return full_text
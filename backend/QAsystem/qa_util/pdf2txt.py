import fitz
import os
import json

PDF_DIR = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/pdf"
OUTPUT_PATH = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/docs"
PROCESSED_PDF_PATH = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/pdf/processed_pdf.json"

def load_processed_pdf():
    if os.path.exists(PROCESSED_PDF_PATH):
        with open(PROCESSED_PDF_PATH, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_pdf(processed_pdf):
    with open(PROCESSED_PDF_PATH, 'w') as f:
        json.dump(list(processed_pdf), f)

def load_pdf(data_dir):
    pdfnames = []
    for pdfname in os.listdir(data_dir):
        if pdfname.endswith('.pdf'):
            pdfnames.append(pdfname)
    return pdfnames

def find_unprocessed_pdfs(folder_path):
    all_pdfnames = load_pdf(folder_path)
    processed_pdf = load_processed_pdf()
    new_pdfnames = [fn for fn in all_pdfnames if fn not in processed_pdf]

    if not new_pdfnames:
        print("✅ 没有新论文，无需处理")

    return new_pdfnames

def extract_text_from_pdf(pdf_path):
    mypdf = fitz.open(pdf_path)
    all_text = ""
    for page_num in range(mypdf.page_count):
        page = mypdf[page_num]
        text = page.get_text("text")
        all_text += text
    return all_text

def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def new_pdf_to_txt(pdf_dir, output_dir):
    new_pdfs = find_unprocessed_pdfs(pdf_dir)
    if not new_pdfs:
        print("✅ 没有新PDF需要转换为TXT。")
        return

    os.makedirs(output_dir, exist_ok=True)
    processed_pdf = load_processed_pdf()  # 别忘了重新加载记录！

    for pdf_name in new_pdfs:
        pdf_path = os.path.join(pdf_dir, pdf_name)
        txt_path = os.path.join(output_dir, pdf_name.replace('.pdf', '.txt'))

        try:
            text = extract_text_from_pdf(pdf_path)
            save_text_to_file(text, txt_path)
            print(f"✅ 已转换: {pdf_name} -> {txt_path}")
            processed_pdf.add(pdf_name)
        except Exception as e:
            print(f"❌ 处理 {pdf_name} 出错: {e}")

    save_processed_pdf(processed_pdf)
    print("✅ 所有新PDF已转换完成并记录。")

def main():
    new_pdf_to_txt(PDF_DIR, OUTPUT_PATH)

if __name__ == "__main__":
    main()
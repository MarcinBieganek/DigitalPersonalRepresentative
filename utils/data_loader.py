from pypdf import PdfReader

def load_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        if content := page.extract_text():
            text += content
    return text

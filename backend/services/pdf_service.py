import fitz  # PDF
from docx import Document  # Word
from pptx import Presentation  # PowerPoint

def extract_text(file_bytes: bytes, filename: str):

    if filename.endswith(".pdf"):
        return extract_pdf(file_bytes)

    elif filename.endswith(".docx"):
        return extract_docx(file_bytes)

    elif filename.endswith(".pptx"):
        return extract_pptx(file_bytes)

    else:
        raise ValueError("Formato no soportado")


# 📄 PDF
def extract_pdf(file_bytes: bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


# 📝 WORD
def extract_docx(file_bytes: bytes):
    from io import BytesIO
    doc = Document(BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])


# 📊 POWERPOINT
def extract_pptx(file_bytes: bytes):
    from io import BytesIO
    prs = Presentation(BytesIO(file_bytes))
    text = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)

    return "\n".join(text)
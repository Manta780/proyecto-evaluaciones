import pytesseract
from PIL import Image
import fitz
import io


def ocr_imagen(file_bytes):
    try:
        imagen = Image.open(io.BytesIO(file_bytes))
        texto = pytesseract.image_to_string(imagen, lang="spa")
        return texto
    except Exception as e:
        print("Error OCR imagen", e)
        return ""
    
def ocr_pdf(file_bytes):
    texto_total = ""

    try: 
        pdf = fitz.open(stream=file_bytes, filetype="pdf")

        for pagina in pdf:
            pix = pagina.get_pixmap()
            img_bytes = pix.tobytes("png")

            imagen = Image.open(io.BytesIO(img_bytes))
            texto = pytesseract.image_to_string(imagen, lang="spa")

            texto_total += texto + "\n"

        return texto_total
    except Exception as e:
        print("Error OCR PDF", e)
        return ""
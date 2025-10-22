import cv2
import pytesseract
from PIL import Image
import re
from fpdf import FPDF
import os

# Make sure Tesseract is installed on your system
# Example for Windows:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    # Read and preprocess
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # OCR
    text = pytesseract.image_to_string(gray)

    # Clean up
    text = re.sub(r'[^A-Za-z0-9.,;:!?()\n\s]', '', text)
    return text.strip()

def save_as_pdf(text, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(output_pdf)
    print(f"✅ PDF saved as {output_pdf}")

if __name__ == "__main__":
    input_image = "samples/note1.jpg"
    output_text_file = "output/note1.txt"
    output_pdf_file = "output/note1.pdf"

    text = extract_text(input_image)

    # Save as text
    os.makedirs("output", exist_ok=True)
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(text)

    # Save as PDF
    save_as_pdf(text, output_pdf_file)
    print("✅ Text extraction complete!")

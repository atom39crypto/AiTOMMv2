import os
import mimetypes

# External libraries
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

# from secondayAI.uploder import uploder  # Ensure this import is correct and the module exists


def describe_image(img):
    """Generate a basic description based on OCR layout and keyword frequency."""
    try:
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        words = [word for word in data['text'] if word.strip()]
        if not words:
            return "The image appears to contain no readable text."

        most_common = max(set(words), key=words.count)
        total_words = len(words)
        description = (
            f"The image likely contains textual content. "
            f"It includes around {total_words} words. "
            f"A frequently occurring word is '{most_common}'."
        )
        return description
    except Exception as e:
        return f"Could not describe image: {e}"


def read_text_from_file(file_path):
    if not os.path.exists(file_path):
        return f"File '{file_path}' not found."

    mime_type, _ = mimetypes.guess_type(file_path)
    extracted_text = []

    try:
        # Text file
        if mime_type and mime_type.startswith('text'):
            with open(file_path, 'r', encoding='utf-8') as f:
                extracted_text.append(f.read())

        # PDF file
        elif file_path.endswith('.pdf'):
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted_text.append(page.extract_text())

        # Word document
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs:
                extracted_text.append(para.text)

        # Image file (OCR + Description)
        elif mime_type and mime_type.startswith('image'):
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            description = describe_image(img)
            extracted_text.append(f"[Image Description]: {description}")
            extracted_text.append("[Extracted Text from Image]:")
            extracted_text.append(text)

        else:
            # Fallback: binary preview
            with open(file_path, 'rb') as f:
                content = f.read(100)
                extracted_text.append(f"Unknown format, binary preview: {content}")

    except Exception as e:
        return f"Error reading or extracting content: {e}"

    print(f"Extracted text from {file_path}:")
    for text in extracted_text:
        print(text)
    return "\n".join(extracted_text)

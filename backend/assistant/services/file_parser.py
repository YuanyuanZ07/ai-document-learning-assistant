import os

from pypdf import PdfReader
from docx import Document as DocxDocument


SUPPORTED_EXTENSIONS = {'.txt', '.pdf', '.docx'}


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()


def extract_text_from_file(file_obj, filename):
    """Extract text content from an uploaded file object."""
    ext = get_file_extension(filename)

    if ext == '.txt':
        return _extract_from_txt(file_obj)
    elif ext == '.pdf':
        return _extract_from_pdf(file_obj)
    elif ext == '.docx':
        return _extract_from_docx(file_obj)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def _extract_from_txt(file_obj):
    return file_obj.read().decode('utf-8')


def _extract_from_pdf(file_obj):
    reader = PdfReader(file_obj)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return '\n'.join(text_parts)


def _extract_from_docx(file_obj):
    doc = DocxDocument(file_obj)
    return '\n'.join(para.text for para in doc.paragraphs if para.text)

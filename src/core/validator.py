import PyPDF2
from src.utils.logger import scanner_logger


def is_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages) > 0
    except Exception as e:
        scanner_logger.error(f"Error validating PDF {file_path}: {str(e)}")
        return False

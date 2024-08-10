from src.utils.file_system import traverse_file_system, get_file_info
from src.core.validator import is_pdf
from src.utils.logger import scanner_logger


def scan_for_pdfs(root_path):
    scanner_logger.info(f"Starting PDF scan from {root_path}")
    pdf_files = []
    for file_path in traverse_file_system(root_path):
        if is_pdf(file_path):
            file_info = get_file_info(file_path)
            if file_info:
                pdf_files.append(file_info)

    pdf_files.sort(key=lambda x: x['modified'], reverse=True)
    scanner_logger.info(f"PDF scan completed. Found {len(pdf_files)} PDF files.")
    return pdf_files

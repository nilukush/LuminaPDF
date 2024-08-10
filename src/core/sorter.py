def sort_pdf_files(pdf_files):
    return sorted(pdf_files, key=lambda x: x['modified'], reverse=True)

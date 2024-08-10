import os
from src.utils.logger import scanner_logger


def traverse_file_system(root_path):
    scanner_logger.info(f"Starting file system traversal from {root_path}")
    for root, dirs, files in os.walk(root_path):
        for file in files:
            yield os.path.join(root, file)
    scanner_logger.info("File system traversal completed")


def get_file_info(file_path):
    try:
        return {
            'path': file_path,
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path)
        }
    except OSError as e:
        scanner_logger.error(f"Error getting file info for {file_path}: {str(e)}")
        return None

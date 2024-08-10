import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
                             QWidget, QFileDialog, QListWidget, QLabel, QScrollArea)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.core.scanner import scan_for_pdfs


class PDFViewerWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWidget(self.label)
        self.current_page = 0
        self.doc = None

    def load_pdf(self, pdf_path):
        self.doc = fitz.open(pdf_path)
        self.current_page = 0
        self.show_page(self.current_page)

    def show_page(self, page_num):
        if self.doc is None:
            return
        page = self.doc.load_page(page_num)
        pix = page.get_pixmap()
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(pixmap)
        self.label.adjustSize()

    def next_page(self):
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)


class ScannerThread(QThread):
    update_progress = pyqtSignal(int)
    scan_complete = pyqtSignal(list)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        pdf_files = scan_for_pdfs(self.path)
        self.scan_complete.emit(pdf_files)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LuminaPDF Reader")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()

        # Left panel for file list and scan button
        left_panel = QVBoxLayout()
        self.scan_button = QPushButton("Select Folder to Scan")
        self.scan_button.clicked.connect(self.start_scan)
        left_panel.addWidget(self.scan_button)

        self.result_list = QListWidget()
        self.result_list.itemClicked.connect(self.load_pdf)
        left_panel.addWidget(self.result_list)

        # Right panel for PDF viewer
        right_panel = QVBoxLayout()
        self.pdf_viewer = PDFViewerWidget()
        right_panel.addWidget(self.pdf_viewer)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous Page")
        self.prev_button.clicked.connect(self.pdf_viewer.prev_page)
        self.next_button = QPushButton("Next Page")
        self.next_button.clicked.connect(self.pdf_viewer.next_page)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        right_panel.addLayout(nav_layout)

        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.scan_button.setEnabled(False)
            self.result_list.clear()

            self.scanner_thread = ScannerThread(folder)
            self.scanner_thread.scan_complete.connect(self.display_results)
            self.scanner_thread.start()

    def display_results(self, pdf_files):
        for pdf in pdf_files:
            self.result_list.addItem(pdf['path'])
        self.scan_button.setEnabled(True)

    def load_pdf(self, item):
        pdf_path = item.text()
        self.pdf_viewer.load_pdf(pdf_path)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

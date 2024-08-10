import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QListWidget, \
    QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal
from src.core.scanner import scan_for_pdfs


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
        self.scanner_thread = None
        self.setWindowTitle("PDF Scanner")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.scan_button = QPushButton("Select Folder to Scan")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.scan_button.setEnabled(False)
            self.progress_bar.setValue(0)
            self.result_list.clear()

            self.scanner_thread = ScannerThread(folder)
            self.scanner_thread.update_progress.connect(self.update_progress)
            self.scanner_thread.scan_complete.connect(self.display_results)
            self.scanner_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_results(self, pdf_files):
        for pdf in pdf_files:
            self.result_list.addItem(f"{pdf['path']} - Last modified: {pdf['modified']}")
        self.scan_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

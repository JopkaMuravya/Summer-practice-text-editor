from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QFileInfo
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = None
        uic.loadUi('Design.ui', self)
        self.setWindowTitle('TextUra')
        self.setCentralWidget(self.textEdit)

        self.actionNew.triggered.connect(self.file_new)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.file_save)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionExit.triggered.connect(self.exit_app)
        self.actionCopy.triggered.connect(self.copy_text)
        self.actionPaste.triggered.connect(self.paste_text)
        self.actionCut.triggered.connect(self.cut_text)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)

    def file_new(self):
        self.textEdit.clear()

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
        if filename[0]:
            f = open(filename[0], 'r', encoding='utf-8')
            with f:
                data = f.read()
                self.textEdit.setText(data)

    def file_save(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File')
        if filename[0]:
            f = open(filename[0], 'w', encoding='utf-8')
            with f:
                text = self.textEdit.toPlainText()
                f.write(text)
                QMessageBox.about(self, "Save File", "File Saved Successfully")

    def export_pdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf) ;; All Files")
        if fn != "":
            if QFileInfo(fn).suffix() == "":fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def exit_app(self):
        self.close()

    def copy_text(self):
        self.textEdit.copy()

    def paste_text(self):
        self.textEdit.paste()

    def cut_text(self):
        self.textEdit.cut()

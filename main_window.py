from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QFont


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
        self.actionFont.triggered.connect(self.font_dialog)
        self.actionColor.triggered.connect(self.color_dialog)
        self.actionBold.triggered.connect(self.text_bold)
        self.actionItalic.triggered.connect(self.text_italic)
        self.actionUnderline.triggered.connect(self.text_underline)
        self.actionLeft.triggered.connect(self.text_left)
        self.actionCenter.triggered.connect(self.text_center)
        self.actionRight.triggered.connect(self.text_right)
        self.actionJustify.triggered.connect(self.text_justify)

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

    def font_dialog(self):
        font, ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

    def color_dialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def text_bold(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def text_italic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def text_underline(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def text_left(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def text_center(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def text_right(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def text_justify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

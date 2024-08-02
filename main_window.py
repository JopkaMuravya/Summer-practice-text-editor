from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QFontDialog, QColorDialog, QInputDialog
from PyQt5.QtCore import QFileInfo, Qt, QRegExp
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QBrush, QColor, QTextBlockFormat
from FontSettingsWidget import FontSettingsWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = None
        uic.loadUi('Design.ui', self)
        self.setWindowTitle('TextUra')
        self.setLayout(self.gridLayout)

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
        self.actionFind.triggered.connect(self.find_text)
        self.actionFind_and_replace.triggered.connect(self.find_and_replace)
        self.spinBoxIndentation.valueChanged.connect(self.indentation)
        self.spinBoxInterval.valueChanged.connect(self.interval)
        self.actionCustom_style.triggered.connect(self.custom_style)

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
            cursor = self.textEdit.textCursor()
            selected_text = cursor.selectedText()
            if selected_text:
                new_font = font
                format = QTextCharFormat()
                format.setFont(new_font)
                cursor.mergeCharFormat(format)
            else:
                self.textEdit.setCurrentFont(font)

    def color_dialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def text_bold(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            weight = QFont.Bold if cursor.charFormat().font().weight() != QFont.Bold else QFont.Normal
            format.setFontWeight(weight)
            cursor.mergeCharFormat(format)

    def text_italic(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontItalic(not cursor.charFormat().fontItalic())
            cursor.mergeCharFormat(format)

    def text_underline(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontUnderline(not cursor.charFormat().fontUnderline())
            cursor.mergeCharFormat(format)

    def text_left(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def text_center(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def text_right(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def text_justify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

    def find_text(self):
        find_text, ok = QInputDialog.getText(self, "Поиск", "Введите текст для поиска:")
        if ok:
            text = self.textEdit.toPlainText()
            regexp = QRegExp(find_text)
            if regexp.isValid():
                cursor = self.textEdit.textCursor()
                format = QTextCharFormat()
                format.setBackground(QBrush(QColor("yellow")))
                cursor.beginEditBlock()
                index = 0
                while True:
                    pos = regexp.indexIn(text, index)
                    if pos == -1:
                        break
                    cursor.setPosition(pos)
                    cursor.setPosition(pos + regexp.matchedLength(), QTextCursor.KeepAnchor)
                    cursor.setCharFormat(format)
                    index = pos + regexp.matchedLength()
                cursor.endEditBlock()
            else:
                QMessageBox.critical(self, "Ошибка", "Ошибка в регулярном выражении")

    def find_and_replace(self):
        find_text, ok = QInputDialog.getText(self, "Найти и заменить", "Найти (регулярное выражение):")
        if ok:
            replace_text, ok = QInputDialog.getText(self, "Найти и заменить", "Заменить на:")
            if ok:
                text = self.textEdit.toPlainText()
                regexp = QRegExp(find_text)
                if regexp.isValid():
                    index = 0
                    while True:
                        pos = regexp.indexIn(text, index)
                        if pos == -1:
                            break
                        text = text[:pos] + replace_text + text[pos + regexp.matchedLength():]
                        index = pos + len(replace_text)
                    self.textEdit.setPlainText(text)
                else:
                    QMessageBox.critical(self, "Ошибка", "Ошибка в регулярном выражении")

    def indentation(self):
        indent_size = self.spinBoxIndentation.value()
        cursor = self.textEdit.textCursor()
        block_format = QTextBlockFormat()
        block_format.setTextIndent(indent_size)
        cursor.mergeBlockFormat(block_format)

    def interval(self):
        line_spacing = self.spinBoxInterval.value()
        format = QTextBlockFormat()
        format.setLineHeight(line_spacing, QTextBlockFormat.ProportionalHeight)
        cursor = self.textEdit.textCursor()
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(format)
        cursor.endEditBlock()
        self.textEdit.setTextCursor(cursor)

    def custom_style(self):
        self.custom = FontSettingsWidget()
        self.custom.show()
        self.custom.apply_button.clicked.connect(self.apply_settings)

    def apply_settings(self):
        self.textEdit.setCurrentFont(self.custom.font)
        self.textEdit.setTextColor(self.custom.color)


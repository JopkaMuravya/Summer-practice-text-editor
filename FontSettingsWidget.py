from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QCheckBox, QPushButton, QColorDialog, QTextEdit
from PyQt5.QtGui import QFont, QColor


class FontSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Font Settings")
        self.setGeometry(300, 300, 400, 350)
        layout = QVBoxLayout()
        self.setLayout(layout)

        family_label = QLabel("Family:")
        self.family_combo = QComboBox()
        self.family_combo.addItem("Arial")
        self.family_combo.addItem("Times New Roman")
        self.family_combo.addItem("Courier")
        layout.addWidget(family_label)
        layout.addWidget(self.family_combo)

        size_label = QLabel("Size:")
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(8)
        self.size_spin.setMaximum(48)
        layout.addWidget(size_label)
        layout.addWidget(self.size_spin)

        style_label = QLabel("Style:")
        self.style_combo = QComboBox()
        self.style_combo.addItem("Regular")
        self.style_combo.addItem("Bold")
        self.style_combo.addItem("Italic")
        self.style_combo.addItem("Bold Italic")
        layout.addWidget(style_label)
        layout.addWidget(self.style_combo)

        effects_label = QLabel("Effects:")
        self.underline_checkbox = QCheckBox("Underline")
        self.strikeout_checkbox = QCheckBox("Strikeout")
        layout.addWidget(effects_label)
        layout.addWidget(self.underline_checkbox)
        layout.addWidget(self.strikeout_checkbox)

        color_label = QLabel("Color:")
        self.color_button = QPushButton("Select Color")
        self.color_button.clicked.connect(self.selectColor)
        layout.addWidget(color_label)
        layout.addWidget(self.color_button)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.applyFontSettings)
        layout.addWidget(self.apply_button)
        self.color = QColor("black")

    def selectColor(self):
        color = QColorDialog.getColor(self.color, self, "Select Color")
        if color.isValid():
            self.color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()}")

    def applyFontSettings(self):
        family = self.family_combo.currentText()
        size = self.size_spin.value()
        style = self.style_combo.currentText()
        underline = self.underline_checkbox.isChecked()
        strikeout = self.strikeout_checkbox.isChecked()
        self.font = QFont(family, size)
        if style == "Bold":
            self.font.setWeight(QFont.Bold)
        elif style == "Italic":
            self.font.setStyle(QFont.StyleItalic)
        elif style == "Bold Italic":
            self.font.setWeight(QFont.Bold)
            self.font.setStyle(QFont.StyleItalic)
        if underline:
            self.font.setUnderline(True)
        if strikeout:
            self.font.setStrikeOut(True)

        self.text_edit.setCurrentFont(self.font)
        self.text_edit.setTextColor(self.color)

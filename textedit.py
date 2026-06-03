import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                             QMenuBar, QMenu, QFileDialog, QMessageBox,
                             QColorDialog, QFontDialog, QToolBar, QComboBox)
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QAction, QColor, QFont, QPainter, QPixmap, QTextDocument


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("cooltextedit")
        self.setGeometry(100, 100, 800, 600)
        
        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)
        
        self.create_menu()
        self.create_toolbar()
    
    def create_menu(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Файл")
        
        open_action = file_menu.addAction("Открыть файл...")
        open_action.triggered.connect(self.open_file)
        
        save_action = file_menu.addAction("Сохранить файл...")
        save_action.triggered.connect(self.save_file)
        
        save_png_action = file_menu.addAction("Сохранить как PNG...")
        save_png_action.triggered.connect(self.save_as_png)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)
        
        format_menu = menu_bar.addMenu("Формат")
        
        color_action = format_menu.addAction("Цвет текста...")
        color_action.triggered.connect(self.change_text_color)
        
        font_action = format_menu.addAction("Шрифт и размер...")
        font_action.triggered.connect(self.change_font)
    
    def create_toolbar(self):
        toolbar = self.addToolBar("Форматирование")
        toolbar.setMovable(False)
        
        color_action = QAction("🎨 Цвет", self)
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)
        
        toolbar.addSeparator()
        
        font_action = QAction("📝 Шрифт", self)
        font_action.triggered.connect(self.change_font)
        toolbar.addAction(font_action)
        
        toolbar.addSeparator()
        
        toolbar.addWidget(self.create_font_size_combo())
        
        toolbar.addSeparator()
        
        increase_font_action = QAction("🔍+", self)
        increase_font_action.triggered.connect(self.increase_font_size)
        toolbar.addAction(increase_font_action)
        
        decrease_font_action = QAction("🔍-", self)
        decrease_font_action.triggered.connect(self.decrease_font_size)
        toolbar.addAction(decrease_font_action)
        
        toolbar.addSeparator()
        
        save_png_action = QAction("📸 Сохранить как PNG", self)
        save_png_action.triggered.connect(self.save_as_png)
        toolbar.addAction(save_png_action)
    
    def create_font_size_combo(self):
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems([str(size) for size in range(8, 73, 2)])
        self.font_size_combo.setCurrentText("12")
        self.font_size_combo.setEditable(True)
        self.font_size_combo.setMaximumWidth(70)
        self.font_size_combo.currentTextChanged.connect(self.change_font_size)
        return self.font_size_combo
    
    def save_as_png(self):
        doc = QTextDocument()
        doc.setDocumentMargin(10)
        doc.setHtml(self.text_area.toHtml())
        
        doc.setTextWidth(self.text_area.viewport().width())
        
        doc_size = doc.size()
        width = int(doc_size.width())
        height = int(doc_size.height())
        
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        doc.drawContents(painter)
        painter.end()
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить как PNG",
            "",
            "PNG Image (*.png);;All files (*.*)"
        )
        
        if filename:
            if not filename.endswith('.png'):
                filename += '.png'
            
            if pixmap.save(filename, "PNG"):
                QMessageBox.information(self, "Успех", f"Файл успешно сохранен как:\n{filename}\n(с прозрачным фоном)")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить изображение")
    
    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_area.setTextColor(color)
    
    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_area.setCurrentFont(font)
            current_size = str(font.pointSize())
            index = self.font_size_combo.findText(current_size)
            if index >= 0:
                self.font_size_combo.setCurrentIndex(index)
            else:
                self.font_size_combo.setCurrentText(current_size)
    
    def change_font_size(self, size_str):
        try:
            size = int(size_str)
            if size >= 1:
                font = self.text_area.currentFont()
                font.setPointSize(size)
                self.text_area.setCurrentFont(font)
        except ValueError:
            pass
    
    def increase_font_size(self):
        current_font = self.text_area.currentFont()
        current_size = current_font.pointSize()
        new_size = current_size + 2
        if new_size <= 72:
            current_font.setPointSize(new_size)
            self.text_area.setCurrentFont(current_font)
            self.font_size_combo.setCurrentText(str(new_size))
    
    def decrease_font_size(self):
        current_font = self.text_area.currentFont()
        current_size = current_font.pointSize()
        new_size = current_size - 2
        if new_size >= 6:
            current_font.setPointSize(new_size)
            self.text_area.setCurrentFont(current_font)
            self.font_size_combo.setCurrentText(str(new_size))
    
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Открыть файл", 
            "", 
            "Text files (*.txt);;All files (*.*)"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_area.setText(content)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Сохранить файл", 
            "", 
            "Text files (*.txt);;All files (*.*)"
        )
        
        if not filename:
            return
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        try:
            text_to_save = self.text_area.toPlainText().strip() + '\n'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text_to_save)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
import sys
import openpyxl


class TextFileLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Ustawienie layoutu i elementów interfejsu
        layout = QVBoxLayout()

        self.path_edit = QLineEdit(self)
        self.path_edit.setPlaceholderText("Wpisz ścieżkę do pliku lub wybierz...")

        self.button = QPushButton("Wybierz plik", self)
        self.button.clicked.connect(self.open_file_dialog)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout.addWidget(self.path_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)
        self.setWindowTitle("Ładowanie pliku tekstowego")
        self.setGeometry(100, 100, 600, 400)

        # Obsługa ręcznie wpisanej ścieżki
        self.path_edit.returnPressed.connect(self.load_from_path)

    def open_file_dialog(self):
        # Otwieranie dialogu wyboru pliku
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik tekstowy", "", "Pliki tekstowe (*.xlsx);;Wszystkie pliki (*)", options=options)

        if file_path:
            self.path_edit.setText(file_path)  # Ustawienie ścieżki w polu tekstowym
            self.plik(file_path)

    def load_from_path(self):
        # Wczytanie pliku z ręcznie wpisanej ścieżki
        file_path = self.path_edit.text()
        if file_path:
            self.plik(file_path)

    def plik(self, file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        sheet_name = sheet.title
        print("Nazwa arkusza:", sheet_name)

        # Oblicz liczbę użytych kolumn
        used_columns = sheet.max_column
        print("Liczba użytych kolumn:", used_columns)

    def load_file(self, file_path):
        # Ładowanie zawartości pliku i wyświetlanie w QTextEdit
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setText(content)
        except Exception as e:
            self.text_edit.setText(f"Nie udało się załadować pliku: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loader = TextFileLoader()
    loader.show()
    sys.exit(app.exec_())

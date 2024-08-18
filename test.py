import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout
import datetime

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Inicjalizacja listy lat
        self.years = [2022, 2023, 2024, 2025, 2026]

        # Inicjalizacja ComboBox
        self.comboBox = QComboBox(self)
        #self.comboBox.addItems([str(year) for year in self.years])
        for year in self.years:
            self.comboBox.addItem(str(year))

        # Pobranie bieżącego roku
        current_year = datetime.datetime.now().year

        # Ustawienie bieżącego roku jako domyślnie wybranej wartości
        if current_year in self.years:
            self.comboBox.setCurrentText(str(current_year))
        else:
            self.comboBox.setCurrentIndex(0)  # domyślnie pierwszy element

        # Układ
        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

        # Konfiguracja okna
        self.setWindowTitle('QComboBox Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
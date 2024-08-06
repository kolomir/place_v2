import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Tworzenie głównego układu pionowego
        self.layout = QVBoxLayout()

        # Tworzenie i dodawanie QComboBox do układu
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Option 1", "Option 2", "Option 3"])
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.layout.addWidget(self.comboBox)

        # Tworzenie i dodawanie pól tekstowych do układu
        self.lineEdits = []
        for i in range(3):
            lineEdit = QLineEdit()
            lineEdit.setPlaceholderText(f"Text Field {i + 1}")
            lineEdit.setDisabled(True)  # Domyślnie wyłączone
            self.layout.addWidget(lineEdit)
            self.lineEdits.append(lineEdit)

        # Ustawienie układu dla głównego QWidget
        self.setLayout(self.layout)

        self.setWindowTitle("QComboBox Example")
        self.show()

    def on_combobox_changed(self, index):
        # Wyłączanie wszystkich pól tekstowych
        for lineEdit in self.lineEdits:
            lineEdit.setDisabled(True)

        # Włączanie odpowiedniego pola tekstowego
        self.lineEdits[index].setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
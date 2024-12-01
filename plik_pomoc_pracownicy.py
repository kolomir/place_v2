from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView
from PyQt5.QtGui import QPixmap

from _plik_pomoc_pracownicy_ui import Ui_Form
import db, dodatki


class MainWindow_pomoc_pracownicy(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.current_image_index = 0
        self.image_paths = ["img/pomoc/01 pracownicy.png", "img/pomoc/02 pracownicy.png"]

        self.update_image()

        self.ui.btn_prev.clicked.connect(self.show_previous_image)
        self.ui.btn_next.clicked.connect(self.show_next_image)

    def update_image(self):
        # Wczytuje obraz do QLabel na podstawie aktualnego indeksu
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.ui.lab_image.setPixmap(pixmap)
        self.ui.lab_image.setScaledContents(True)

    def show_next_image(self):
        # Przechodzi do następnego obrazu
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.update_image()

    def show_previous_image(self):
        # Przechodzi do poprzedniego obrazu
        self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
        self.update_image()
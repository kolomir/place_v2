from PyQt5.QtWidgets import QWidget, QMessageBox

from _pracownicy_magDodaj_ui import Ui_Form
import db

class MainWindow_pracownicy_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def otworz_okno_pracownicy_magDodaj(self):
        self.okno_pracownicy_magDodaj = MainWindow_pracownicy_magDodaj()
        self.okno_pracownicy_magDodaj.show()
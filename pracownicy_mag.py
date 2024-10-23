from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _pracownicy_mag_ui import Ui_Form
import db

from pracownicy_magDodaj import MainWindow_pracownicy_magDodaj
from linieFormEdytuj import MainWindow_linieEdytuj

class MainWindow_pracownicy_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_pracownicy_magDodaj)

    def otworz_okno_pracownicy_magDodaj(self):
        self.okno_pracownicy_magDodaj = MainWindow_pracownicy_magDodaj()
        self.okno_pracownicy_magDodaj.show()
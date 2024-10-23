from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QHeaderView,QApplication
from PyQt5.QtCore import pyqtSlot, Qt

from _grupy_mag_ui import Ui_Form
import db

from grupy_magDodaj import MainWindow_grupy_magDodaj

class MainWindow_grupy_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.otworz_okno_grupy_magDodaj)

    def otworz_okno_grupy_magDodaj(self):
        self.okno_grupy_magDodaj = MainWindow_grupy_magDodaj()
        self.okno_grupy_magDodaj.show()
from PyQt5.QtWidgets import QWidget, QMessageBox

from _grupy_magDodaj_ui import Ui_Form
import db

class MainWindow_grupy_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
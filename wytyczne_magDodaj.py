from PyQt5.QtWidgets import QWidget, QMessageBox

from _wytyczne_magDodaj_ui import Ui_Form
import db

class MainWindow_wytyczne_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def otworz_okno_wytyczne_magDodaj(self):
        self.okno_wytyczne_magDodaj = MainWindow_wytyczne_magDodaj()
        self.okno_wytyczne_magDodaj.show()
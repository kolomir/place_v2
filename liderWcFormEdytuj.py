from PyQt5.QtWidgets import QWidget, QMessageBox

from _liderWcFormEdytuj_ui import Ui_Form
import db

class MainWindow_liderWcEdytuj(QWidget):
    def __init__(self, data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
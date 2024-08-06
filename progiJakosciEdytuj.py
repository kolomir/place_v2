from PyQt5.QtWidgets import QWidget, QMessageBox

from _progiJakosciEdytuj_ui import Ui_Form
import db

class MainWindow_progiJakosciEdytuj(QWidget):
    def __init__(self,data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
from PyQt5.QtWidgets import QWidget

from _ustawieniaMenu_mag_ui import Ui_Form

from lokalizacjeForm import MainWindow_lokalizacje
from wytyczne_mag import MainWindow_wytyczne_mag
from pracownicy_mag import MainWindow_pracownicy_mag
from grupy_mag import MainWindow_grupy_mag

class MainWindow_ustawienia_mag(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_lokalizacje.clicked.connect(self.otworz_okno_lokalizacjeForm)
        self.ui.btn_grupy.clicked.connect(self.otworz_okno_grupy_mag)
        self.ui.btn_pracownicy.clicked.connect(self.otworz_okno_pracownicy_mag)
        self.ui.btn_wytyczne_mag.clicked.connect(self.otworz_okno_wytyczne_mag)

    def otworz_okno_lokalizacjeForm(self):
        self.okno_lokalizacjeForm = MainWindow_lokalizacje()
        self.okno_lokalizacjeForm.show()

    def otworz_okno_grupy_mag(self):
        self.okno_grupy_mag = MainWindow_grupy_mag()
        self.okno_grupy_mag.show()

    def otworz_okno_pracownicy_mag(self):
        self.okno_pracownicy_mag = MainWindow_pracownicy_mag()
        self.okno_pracownicy_mag.show()

    def otworz_okno_wytyczne_mag(self):
        self.okno_wytyczne_mag = MainWindow_wytyczne_mag()
        self.okno_wytyczne_mag.show()
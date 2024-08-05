from PyQt5.QtWidgets import QWidget

from _ustawieniaMenu_ui import Ui_Form

from lokalizacjeForm import MainWindow_lokalizacje
from linieForm import MainWindow_linie
from wcForm import MainWindow_wc
from wcliniaForm import MainWindow_wclinia
from liderzyForm import MainWindow_liderzy
from progiProduktywnosci import MainWindow_progiProduktywnosci


class MainWindow_ustawienia(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_lokalizacje.clicked.connect(self.otworz_okno_lokalizacjeForm)
        self.ui.btn_linie.clicked.connect(self.otworz_okno_linieForm)
        self.ui.btn_wc.clicked.connect(self.otworz_okno_wcForm)
        self.ui.btn_linie_wc.clicked.connect(self.otworz_okno_wcliniaForm)
        self.ui.btn_liderzy.clicked.connect(self.otworz_okno_liderzyForm)
        self.ui.btn_progiProd.clicked.connect(self.otworz_okno_progiProduktywnosci)

    def otworz_okno_lokalizacjeForm(self):
        self.okno_lokalizacjeForm = MainWindow_lokalizacje()
        self.okno_lokalizacjeForm.show()

    def otworz_okno_linieForm(self):
        self.okno_linieForm = MainWindow_linie()
        self.okno_linieForm.show()

    def otworz_okno_wcForm(self):
        self.okno_wcForm = MainWindow_wc()
        self.okno_wcForm.show()

    def otworz_okno_wcliniaForm(self):
        self.okno_wcliniaForm = MainWindow_wclinia()
        self.okno_wcliniaForm.show()

    def otworz_okno_liderzyForm(self):
        self.okno_liderzyForm = MainWindow_liderzy()
        self.okno_liderzyForm.show()

    def otworz_okno_progiProduktywnosci(self):
        self.okno_progiProduktywnosci = MainWindow_progiProduktywnosci()
        self.okno_progiProduktywnosci.show()

from PyQt5.QtWidgets import QWidget

from _ustawieniaMenu_ui import Ui_Form

from lokalizacjeForm import MainWindow_lokalizacje
from linieForm import MainWindow_linie
from wcForm import MainWindow_wc
from wcliniaForm import MainWindow_wclinia
from liderzyForm import MainWindow_liderzy
from progiProduktywnosci import MainWindow_progiProduktywnosci
from progiJakosci import MainWindow_progiJakosci
from kwotyJakoscForm import MainWindow_kwotyJakosc
from liderWcForm import MainWindow_liderWc
from dniPracujaceForm import MainWindow_dniPracujaceForm
from pomocForm import MainWindow_pomocForm


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
        self.ui.btn_progiJak.clicked.connect(self.otworz_okno_progiJakosci)
        self.ui.btn_kwoty.clicked.connect(self.otworz_okno_kwotyJakosc)
        self.ui.btn_instruktorzy.clicked.connect(self.otworz_okno_liderWcForm)
        self.ui.btn_dniPracujace.clicked.connect(self.otworz_okno_dniPracujaceForm)
        self.ui.btn_pomoc.clicked.connect(self.otworz_okno_pomocForm)

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

    def otworz_okno_progiJakosci(self):
        self.okno_progiJakosci = MainWindow_progiJakosci()
        self.okno_progiJakosci.show()

    def otworz_okno_kwotyJakosc(self):
        self.okno_kwotyJakosc = MainWindow_kwotyJakosc()
        self.okno_kwotyJakosc.show()

    def otworz_okno_liderWcForm(self):
        self.okno_liderWcForm = MainWindow_liderWc()
        self.okno_liderWcForm.show()

    def otworz_okno_dniPracujaceForm(self):
        self.okno_dniPracujaceForm = MainWindow_dniPracujaceForm()
        self.okno_dniPracujaceForm.show()

    def otworz_okno_pomocForm(self):
        self.okno_pomocForm = MainWindow_pomocForm()
        self.okno_pomocForm.show()

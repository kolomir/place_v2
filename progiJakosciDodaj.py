from PyQt5.QtWidgets import QWidget, QMessageBox

from _progiJakosciDodaj_ui import Ui_Form
import db
from datetime import datetime

class MainWindow_progiJakosciDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.combo_ranga()
        self.combo_lokalizacja()
        self.combo_wc()
        self.ui.combo_lokalizacja.setEnabled(False)
        self.ui.combo_wc.setEnabled(False)
        #self.ui.combo_ranga.currentIndexChanged.connect(self.on_combobox_changed)
        self.ui.combo_ranga.currentIndexChanged.connect(self.on_combo_ranga_changed)

    def combo_ranga(self):
        select_data_ranga = "SELECT * FROM ranga;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)

        id = 0
        value = '-----'
        self.ui.combo_ranga.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_ranga.addItem(value, id)

    def combo_lokalizacja(self):
        select_data_ranga = "SELECT * FROM lokalizacja WHERE aktywny = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)

        id = 0
        value = '-----'
        self.ui.combo_lokalizacja.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_lokalizacja.addItem(value, id)

    def combo_wc(self):
        select_data_ranga = "SELECT * FROM gniazda_robocze WHERE aktywna = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)

        id = 0
        value = '-----'
        self.ui.combo_wc.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_wc.addItem(value, id)

    def on_combo_ranga_changed(self, index):
        print('index:',index)
        if index == 1:
            self.ui.combo_lokalizacja.setEnabled(True)
            self.ui.combo_wc.setEnabled(False)
            select_data_ranga = "SELECT * FROM gniazda_robocze WHERE aktywna = 1;"
        if index == 2:
            self.ui.combo_lokalizacja.setEnabled(False)
            self.ui.combo_wc.setEnabled(True)
            select_data_ranga = "SELECT * FROM gniazda_robocze WHERE aktywna = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)
        # TODO: w funkcji "on_combo_ranga_changed()" w warunkach można dodać automatycznie kwotę dla danej rangi. Pole kwoty nie jest edytowalne
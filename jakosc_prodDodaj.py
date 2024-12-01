from PyQt5.QtWidgets import QWidget, QMessageBox

from _jakosc_prodDodaj_ui import Ui_Form
import db, dodatki
from datetime import datetime

class MainWindow_jakosc_prodDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.combo_gniazda()
        self.combo_ranga()
        self.combo_lokalizacja()
        self.ui.combo_ranga.currentIndexChanged.connect(self.on_combo_ranga_changed)
        self.ui.btn_zapisz.clicked.connect(self.zapisz)

    def combo_ranga(self):
        select_data_ranga = "SELECT * FROM ranga WHERE id = 1 or id = 2;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)

        id = 0
        value = 'Wybierz rangę'
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
        value = 'Wybierz lokalizację'
        self.ui.combo_lokalizacje.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_lokalizacje.addItem(value, id)

    def combo_gniazda(self):
        select_data_ranga = "SELECT * FROM gniazda_robocze WHERE aktywna = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)

        id = 0
        value = 'Wybierz grupę roboczą'
        self.ui.combo_gniazda.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_gniazda.addItem(value, id)

    def on_combo_ranga_changed(self, index):
        print('index:', index)
        if index == 1:
            self.ui.combo_lokalizacje.setEnabled(True)
            self.ui.combo_gniazda.setEnabled(False)
        if index == 2:
            self.ui.combo_lokalizacje.setEnabled(False)
            self.ui.combo_gniazda.setEnabled(True)

    def sprawdz_pole(self):
        self.pole_ranga = self.ui.combo_ranga.currentData()
        pole_wc = self.ui.combo_gniazda.currentData()
        pole_lokalizacja = self.ui.combo_lokalizacje.currentData()
        pole_ppm = self.ui.text_ppm.text().strip()
        pole_reklamacje = self.ui.text_reklamacje.text().strip()

        if self.pole_ranga == 0:
            QMessageBox.critical(self, 'Error', 'Wybierz rangę przełożonego')
            self.ui.combo_ranga.setFocus()
            return False
        if self.pole_ranga == 1:
            if pole_lokalizacja == 0:
                QMessageBox.critical(self, 'Error', 'Wybierz lokalizację przełożonego')
                self.ui.combo_ranga.setFocus()
                return False
        if self.pole_ranga == 2:
            if pole_wc == 0:
                QMessageBox.critical(self, 'Error', 'Wybierz Grupę roboczą')
                self.ui.combo_ranga.setFocus()
                return False
        if not pole_ppm:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole PPM')
            self.ui.text_ppm.setFocus()
            return False
        if not pole_reklamacje:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Reklamacje')
            self.ui.text_reklamacje.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        teraz = datetime.today()
        data_miesiac = str(dodatki.data_miesiac_dzis())

        pole_ranga = self.ui.combo_ranga.currentText()
        pole_wc = self.ui.combo_gniazda.currentText()
        pole_lokalizacja = self.ui.combo_lokalizacje.currentText()
        pole_ppm = self.ui.text_ppm.text().strip()
        pole_reklamacje = self.ui.text_reklamacje.text().strip()

        if self.pole_ranga == 1:
            pole_grupa = pole_lokalizacja
        if self.pole_ranga == 2:
            pole_grupa = pole_wc


        insert_data = "INSERT INTO jakosc_prod VALUES (NULL,'%s','%s','%s','%s','%s','%s');" % (pole_ranga, pole_grupa, pole_ppm, pole_reklamacje, data_miesiac, teraz)
        print(insert_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
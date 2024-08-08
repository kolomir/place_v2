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

        self.ui.btn_zapisz.clicked.connect(self.zapisz)

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
            select_data_ranga = "SELECT * FROM kwoty_jakosc WHERE id_ranga = 1;"
        if index == 2:
            self.ui.combo_lokalizacja.setEnabled(False)
            self.ui.combo_wc.setEnabled(True)
            select_data_ranga = "SELECT * FROM kwoty_jakosc WHERE id_ranga = 2;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)
        self.ui.text_kwota.setText(str(results[0][2]))



    def sprawdz_pole(self):
        pole_ranga = self.ui.combo_ranga.currentData()
        pole_wc = self.ui.combo_wc.currentData()
        pole_lokalizacja = self.ui.combo_lokalizacja.currentData()
        pole_prog1 = self.ui.text_prog1.text().strip()
        pole_prog2 = self.ui.text_prog2.text().strip()
        pole_prog3 = self.ui.text_prog3.text().strip()

        if pole_ranga == 0:
            QMessageBox.critical(self, 'Error', 'Wybierz rangę przełożonego')
            self.ui.combo_ranga.setFocus()
            return False
        if pole_ranga == 1:
            if pole_lokalizacja == 0:
                QMessageBox.critical(self, 'Error', 'Wybierz lokalizację przełożonego')
                self.ui.combo_ranga.setFocus()
                return False
        if pole_ranga == 2:
            if pole_wc == 0:
                QMessageBox.critical(self, 'Error', 'Wybierz Grupę roboczą')
                self.ui.combo_ranga.setFocus()
                return False
        if not pole_prog1:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota')
            self.ui.text_prog1.setFocus()
            return False
        if not pole_prog2:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota')
            self.ui.text_prog2.setFocus()
            return False
        if not pole_prog3:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota')
            self.ui.text_prog3.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_ranga_id = self.ui.combo_ranga.currentData()
        pole_wc_id = self.ui.combo_wc.currentData()
        pole_lokalizacja_id = self.ui.combo_lokalizacja.currentData()
        pole_prog1 = self.ui.text_prog1.text().strip()
        pole_prog2 = self.ui.text_prog2.text().strip()
        pole_prog3 = self.ui.text_prog3.text().strip()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        teraz = datetime.today()
        insert_data1 = "INSERT INTO progi_jakosc VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (pole_lokalizacja_id,pole_wc_id,pole_ranga_id,pole_prog1,pole_prog2,pole_prog3, str(aktywny), teraz)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data1)
        connection.close()
        self.close()
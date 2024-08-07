from PyQt5.QtWidgets import QWidget, QMessageBox

from _kwotyJakoscFormDodaj_ui import Ui_Form
import db
from datetime import datetime

class MainWindow_kwotyJakoscFormDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.combo_ranga()

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

    def sprawdz_pole(self):
        pole_ranga = self.ui.combo_ranga.currentData()
        pole_kwota = self.ui.text_kwota.text().strip()

        if not pole_ranga:
            QMessageBox.critical(self, 'Error', 'Wybierz rangę przełożonego')
            self.ui.combo_ranga.setFocus()
            return False
        if not pole_kwota:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota')
            self.ui.text_kwota.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_ranga_id = self.ui.combo_ranga.currentData()
        pole_kwota = self.ui.text_kwota.text().strip()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        teraz = datetime.today()
        insert_data1 = "INSERT INTO kwoty_jakosc VALUES (NULL, '%s', '%s', '%s', '%s', '%s');" % (pole_ranga_id, pole_kwota, str(aktywny), teraz, None)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data1)
        connection.close()
        self.close()
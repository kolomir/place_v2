from PyQt5.QtWidgets import QWidget, QMessageBox

from _progiProduktywnosciDodaj_ui import Ui_Form
import db
from datetime import datetime

class MainWindow_progiProduktywnosciDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.combo_ranga()

    def combo_ranga(self):
        select_data_ranga = "SELECT * FROM ranga WHERE aktywny = 1;"
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
        pole_prog1 = self.ui.text_prog1.text().strip()
        pole_prog2 = self.ui.text_prog2.text().strip()
        pole_prog3 = self.ui.text_prog3.text().strip()
        pole_kwota1 = self.ui.text_kwota1.text().strip()
        pole_kwota2 = self.ui.text_kwota2.text().strip()
        pole_kwota3 = self.ui.text_kwota3.text().strip()

        if not pole_ranga:
            QMessageBox.critical(self, 'Error', 'Wybierz rangę przełożonego')
            self.ui.combo_ranga.setFocus()
            return False
        if not pole_prog1:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Próg 1')
            self.ui.text_prog1.setFocus()
            return False
        if not pole_prog2:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Próg 2')
            self.ui.text_prog2.setFocus()
            return False
        if not pole_prog3:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Próg 3')
            self.ui.text_prog3.setFocus()
            return False
        if not pole_kwota1:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota 1')
            self.ui.text_kwota1.setFocus()
            return False
        if not pole_kwota2:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota 2')
            self.ui.text_kwota2.setFocus()
            return False
        if not pole_kwota3:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota 3')
            self.ui.text_kwota3.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_ranga_id = self.ui.combo_ranga.currentData()
        pole_prog1 = self.ui.text_prog1.text().strip()
        pole_prog2 = self.ui.text_prog2.text().strip()
        pole_prog3 = self.ui.text_prog3.text().strip()
        pole_kwota1 = self.ui.text_kwota1.text().strip()
        pole_kwota2 = self.ui.text_kwota2.text().strip()
        pole_kwota3 = self.ui.text_kwota3.text().strip()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        teraz = datetime.today()
        print('aktywny:', aktywny)
        insert_data1 = "INSERT INTO instruktor VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (pole_ranga_id, pole_prog1, pole_kwota1, pole_prog2, pole_kwota2, pole_prog3, pole_kwota3, str(aktywny), teraz)
        print(insert_data1)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data1)
        connection.close()
        self.close()
from PyQt5.QtWidgets import QWidget, QMessageBox

from _wytyczne_magDodaj_ui import Ui_Form
import db
from datetime import datetime

class MainWindow_wytyczne_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.combo_grupa()

    def otworz_okno_wytyczne_magDodaj(self):
        self.okno_wytyczne_magDodaj = MainWindow_wytyczne_magDodaj()
        self.okno_wytyczne_magDodaj.show()

    def combo_grupa(self):
        select_data_ranga = "SELECT * FROM grupy_mag where aktywne = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data_ranga)

        id = 0
        value = '-----'
        self.ui.combo_grupa.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_grupa.addItem(value, id)

    def sprawdz_pole(self):
        pole_kwota = self.ui.text_kwota.text().strip()
        pole_nazwa_1 = self.ui.text_nazwa_1.text().strip()
        pole_target_1 = self.ui.text_target_1.text().strip()
        pole_jednostka_1 = self.ui.text_jednostka_1.text().strip()
        combo_grupa = self.ui.combo_grupa.currentData()

        if not pole_kwota:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole z kwotą')
            self.ui.text_kwota.setFocus()
            return False
        if not pole_nazwa_1:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Nazwa KPI')
            self.ui.text_nazwa_1.setFocus()
            return False
        if not pole_target_1:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Target')
            self.ui.text_target_1.setFocus()
            return False
        if not pole_jednostka_1:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Jednostka')
            self.ui.text_jednostka_1.setFocus()
            return False
        if not combo_grupa:
            QMessageBox.critical(self, 'Error', 'Wybierz grupę dla której jest KPI')
            self.ui.combo_grupa.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_kwota = self.ui.text_kwota.text().strip()
        pole_nazwa_1 = self.ui.text_nazwa_1.text().strip()
        pole_target_1 = self.ui.text_target_1.text().strip()
        pole_jednostka_1 = self.ui.text_jednostka_1.text().strip()
        pole_nazwa_2 = self.ui.text_nazwa_2.text().strip()
        pole_target_2 = self.ui.text_target_2.text().strip()
        pole_jednostka_2 = self.ui.text_jednostka_2.text().strip()
        pole_grupa_id = self.ui.combo_grupa.currentData()
        pole_grupa_text = self.ui.combo_grupa.currentText()
        teraz = datetime.today()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        insert_data = "INSERT INTO wytyczne_mag VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (pole_grupa_id,pole_nazwa_1,pole_target_1,pole_jednostka_1,pole_nazwa_2,pole_target_2,pole_jednostka_2,pole_kwota,str(aktywny),teraz)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
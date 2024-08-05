from PyQt5.QtWidgets import QWidget, QMessageBox

from _liderzyFormEdytuj_ui import Ui_Form
import db

class MainWindow_liderzyEdytuj(QWidget):
    def __init__(self,data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_data = data[0]
        self.nrAkt_data = data[1]
        self.nazwisko_data = data[2]
        self.imie_data = data[3]
        self.ranga_data = data[4]
        self.aktywny_data = data[5]

        self.ui.btn_zapisz.clicked.connect(self.zapisz)

        self.combo_ranga()
        self.edytuj()

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

    def edytuj(self):
        select_data = "select id_ranga from instruktor where id = %s;" % int(self.id_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, select_data)

        self.ui.text_nr_akt.setText(self.nrAkt_data)
        self.ui.text_imie.setText(self.imie_data)
        self.ui.text_nazwisko.setText(self.nazwisko_data)
        self.ui.check_aktywny.setChecked(bool(int(self.aktywny_data)))
        self.ui.combo_ranga.setCurrentIndex(int(results[0][0]))

    def sprawdz_pole(self):
        pole_imie = self.ui.text_imie.text().strip()
        pole_nazwisko = self.ui.text_nazwisko.text().strip()
        pole_nrAkt = self.ui.text_nr_akt.text().strip()
        pole_ranga = self.ui.combo_ranga.currentData()

        if not pole_imie:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Imię')
            self.ui.text_imie.setFocus()
            return False
        if not pole_nazwisko:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Nazwisko')
            self.ui.text_nazwisko.setFocus()
            return False
        if not pole_nrAkt:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Nr akt')
            self.ui.text_nr_akt.setFocus()
            return False
        if not pole_ranga:
            QMessageBox.critical(self, 'Error', 'Wybierz rangę przełożonego')
            self.ui.combo_ranga.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_imie = self.ui.text_imie.text().strip()
        pole_nazwisko = self.ui.text_nazwisko.text().strip()
        pole_nrAkt = self.ui.text_nr_akt.text().strip()
        pole_ranga_id = self.ui.combo_ranga.currentData()
        pole_ranga_text = self.ui.combo_ranga.currentText()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        insert_data = "UPDATE instruktor SET nr_akt = '%s', imie = '%s', nazwisko = '%s', aktywny = '%s', id_ranga = '%s' WHERE instruktor.id = '%s';" % (pole_nrAkt,pole_imie,pole_nazwisko,aktywny,pole_ranga_id,self.id_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()

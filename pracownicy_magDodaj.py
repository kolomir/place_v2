from PyQt5.QtWidgets import QWidget, QMessageBox

from _pracownicy_magDodaj_ui import Ui_Form
import db

class MainWindow_pracownicy_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.combo_grupa()
        self.combo_zmiana()

    def otworz_okno_pracownicy_magDodaj(self):
        self.okno_pracownicy_magDodaj = MainWindow_pracownicy_magDodaj()
        self.okno_pracownicy_magDodaj.show()

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

    def combo_zmiana(self):
        self.ui.combo_zmiana.addItem('-----')
        self.ui.combo_zmiana.addItem('A')
        self.ui.combo_zmiana.addItem('B')
        self.ui.combo_zmiana.addItem('C')

    def sprawdz_pole(self):
        pole_imie = self.ui.text_imie.text().strip()
        pole_nazwisko = self.ui.text_nazwisko.text().strip()
        pole_nrAkt = self.ui.text_nr_akt.text().strip()
        pole_grupa = self.ui.combo_grupa.currentData()

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
        if not pole_grupa:
            QMessageBox.critical(self, 'Error', 'Wybierz rangę przełożonego')
            self.ui.combo_grupa.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_imie = self.ui.text_imie.text().strip()
        pole_nazwisko = self.ui.text_nazwisko.text().strip()
        pole_nrAkt = self.ui.text_nr_akt.text().strip()
        pole_grupa_id = self.ui.combo_grupa.currentData()
        pole_grupa_text = self.ui.combo_grupa.currentText()
        pole_zmiana_text = self.ui.combo_zmiana.currentText()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        insert_data = "INSERT INTO pracownicy_mag VALUES (NULL, '%s', '%s', '%s', '%s', '%s', 0, '%s');" % (str(pole_nrAkt), pole_nazwisko, pole_imie, str(aktywny),pole_grupa_id,pole_zmiana_text)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
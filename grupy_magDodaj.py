from PyQt5.QtWidgets import QWidget, QMessageBox

from _grupy_magDodaj_ui import Ui_Form
import db

class MainWindow_grupy_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.combo_lokalizacja()

    def sprawdz_pole(self):
        pole_grupa = self.ui.text_grupa.text().strip()
        pole_lokalizacja = self.ui.combo_lokalizacja.currentData()

        if not pole_grupa:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole z nazwą grupy')
            self.ui.pole_grupa.setFocus()
            return False

        if not pole_lokalizacja:
            QMessageBox.critical(self, 'Error', 'Wybierz lokalizację')
            self.ui.pole_lokalizacja.setFocus()
            return False
        return True

    def combo_lokalizacja(self):
        query = "SELECT * FROM lokalizacja WHERE aktywny = 1;"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results = db.read_query(connection, query)

        id = 0
        value = '-----'
        self.ui.combo_lokalizacja.addItem(value, id)

        for wynik in results:
            id = wynik[0]
            value = wynik[1]
            self.ui.combo_lokalizacja.addItem(value, id)

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_grupa = self.ui.text_grupa.text().strip()
        pole_lokalizacja = self.ui.combo_lokalizacja.currentData()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        insert_data = "INSERT INTO grupy_mag VALUES (NULL, '%s', '%s', 0, '%s');" % (pole_grupa, str(aktywny),pole_lokalizacja)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
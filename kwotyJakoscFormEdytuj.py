from PyQt5.QtWidgets import QWidget, QMessageBox

from _kwotyJakoscFormEdytuj_ui import Ui_Form
import db
from datetime import datetime

class MainWindow_kwotyJakoscFormEdytuj(QWidget):
    def __init__(self,data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_data = data[0]
        self.ranga_data = data[1]
        self.kwota_data = data[2]
        self.aktywny_data = data[3]

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.edytuj()

    def edytuj(self):
        self.ui.text_kwota.setText(self.kwota_data)
        self.ui.lab_ranga.setText(self.ranga_data)
        self.ui.check_aktywny.setChecked(bool(int(self.aktywny_data)))

    def sprawdz_pole(self):
        pole_kwota = self.ui.text_kwota.text().strip()

        if not pole_kwota:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Kwota')
            self.ui.pole_kwota.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_kwota = self.ui.text_kwota.text().strip()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        teraz = datetime.today()
        insert_data = "UPDATE kwoty_jakosc SET kwota = '%s', aktywny = '%s', data_edycji = '%s' WHERE kwoty_jakosc.id = '%s';" % (pole_kwota,str(aktywny),teraz,self.id_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
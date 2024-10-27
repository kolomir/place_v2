from PyQt5.QtWidgets import QWidget, QMessageBox

from _kpi_magDodaj_ui import Ui_Form
import db, dodatki
from datetime import datetime

class MainWindow_kpi_magDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)

    def sprawdz_pole(self):
        pole_delivery = self.ui.text_delivery.text().strip()
        pole_reklamacje = self.ui.text_reklamacje.text().strip()
        pole_dp_init = self.ui.text_dp_init.text().strip()
        pole_zgodnosc = self.ui.text_zgodnosc.text().strip()
        pole_zapasy = self.ui.text_zapasy.text().strip()
        pole_raportowanie = self.ui.text_raportowanie.text().strip()

        if not pole_delivery:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Delivery (poz, 50)')
            self.ui.text_delivery.setFocus()
            return False
        if not pole_reklamacje:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Reklamacje')
            self.ui.text_reklamacje.setFocus()
            return False
        if not pole_dp_init:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole DP po initial (poz, 49)')
            self.ui.text_dp_init.setFocus()
            return False
        if not pole_zgodnosc:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Zgodność stanów na materiałach pomocniczych')
            self.ui.text_zgodnosc.setFocus()
            return False
        if not pole_zapasy:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Zapasy na lokalizacji *** dla wyrobów got. ')
            self.ui.text_zapasy.setFocus()
            return False
        if not pole_raportowanie:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Raportowanie operacji przychodu z produkcji na 104')
            self.ui.text_raportowanie.setFocus()
            return False
        return True

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_delivery = self.ui.text_delivery.text().strip()
        pole_reklamacje = self.ui.text_reklamacje.text().strip()
        pole_dp_init = self.ui.text_dp_init.text().strip()
        pole_zgodnosc = self.ui.text_zgodnosc.text().strip()
        pole_zapasy = self.ui.text_zapasy.text().strip()
        pole_zapasy = pole_zapasy.replace(",", ".")
        pole_raportowanie = self.ui.text_raportowanie.text().strip()
        pole_raportowanie = pole_raportowanie.replace(",", ".")

        teraz = datetime.today()
        miestac = dodatki.data_miesiac_dzis()

        insert_data = "INSERT INTO kpi_mag VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(pole_delivery), str(pole_reklamacje), str(pole_dp_init), str(pole_zgodnosc), str(pole_zapasy), str(pole_raportowanie), miestac, teraz)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
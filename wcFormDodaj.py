from PyQt5.QtWidgets import QWidget, QMessageBox

from _wcFormDodaj_ui import Ui_Form
import db

class MainWindow_wcDodaj(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.btn_zapisz.clicked.connect(self.zapisz)

    def sprawdz_pole(self):
        pole_linie = self.ui.text_linia.text().strip()

        if not pole_linie:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole z nazwą gniazda')
            self.ui.text_linia.setFocus()
            return False
        return True


    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_linie = self.ui.text_linia.text().strip()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        print('aktywny:',aktywny)
        insert_data = "INSERT INTO gniazda_robocze VALUES (NULL, '%s', '%s');" % (pole_linie, str(aktywny))
        print(insert_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
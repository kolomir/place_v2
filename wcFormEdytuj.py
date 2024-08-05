from PyQt5.QtWidgets import QWidget, QMessageBox

from _wcFormEdytuj_ui import Ui_Form
import db

class MainWindow_wcEdytuj(QWidget):
    def __init__(self, data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        print('data:',data)
        self.id_dane = data[0]
        self.edytuj(data)
        self.ui.btn_zapisz.clicked.connect(self.zapisz)

    def edytuj(self,data):
        id_data = data[0]
        nazwa_data = data[1]
        aktywny_data = int(data[2])

        print('id_data:',id_data,'; nazwa_data:',nazwa_data,'; aktywny_data:',aktywny_data )
        print('------------------------------')
        self.ui.text_linia.setText(nazwa_data)
        self.ui.check_aktywny.setChecked(bool(aktywny_data))

    def zapisz(self):
        if not self.sprawdz_pole():
            return

        pole_linie = self.ui.text_linia.text().strip()
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        insert_data = "UPDATE gniazda_robocze SET nazwa = '%s', aktywna = '%s' WHERE gniazda_robocze.id = '%s';" % (pole_linie,aktywny,self.id_dane)
        print(insert_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()

    def sprawdz_pole(self):
        pole_linie = self.ui.text_linia.text().strip()

        if not pole_linie:
            QMessageBox.critical(self, 'Error', 'Uzupełnij pole Linii')
            self.ui.pole_linie.setFocus()
            return False
        return True
from PyQt5.QtWidgets import QWidget, QMessageBox

from _progiProduktywnosciEdytuj_ui import Ui_Form
import db

class MainWindow_progiProduktywnosciEdytuj(QWidget):
    def __init__(self,data):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_data = data[0]
        self.ranga_data = data[1]
        self.prog1_data = data[2]
        self.kwota1_data = data[3]
        self.prog2_data = data[4]
        self.kwota2_data = data[5]
        self.prog3_data = data[6]
        self.kwota3_data = data[7]
        self.aktywny_data = data[8]

        print("id_data: {0}; ranga_data: {1}; prog1_data: {2}; kwota1_data: {3}; prog2_data: {4}; kwota2_data: {5}; prog3_data: {6}; kwota3_data: {7}; aktywny_data: {8};".format(self.id_data, self.ranga_data, self.prog1_data, self.kwota1_data, self.prog2_data, self.kwota2_data, self.prog3_data, self.kwota3_data, self.aktywny_data))

        self.ui.btn_zapisz.clicked.connect(self.zapisz)
        self.edytuj()

    def edytuj(self):
        self.ui.lab_ranga.setText(self.ranga_data)
        self.ui.lab_prog1.setText(self.prog1_data)
        self.ui.lab_kwota1.setText(self.kwota1_data)
        self.ui.lab_prog2.setText(self.prog2_data)
        self.ui.lab_kwota2.setText(self.kwota2_data)
        self.ui.lab_prog3.setText(self.prog3_data)
        self.ui.lab_kwota3.setText(self.kwota3_data)
        self.ui.check_aktywny.setChecked(bool(int(self.aktywny_data)))

    def zapisz(self):
        if self.ui.check_aktywny.isChecked():
            aktywny = 1
        else:
            aktywny = 0
        insert_data = "UPDATE progi_prod SET aktywny = '%s' WHERE progi_prod.id = '%s';" % (str(aktywny),self.id_data)
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        db.execute_query(connection, insert_data)
        connection.close()
        self.close()
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem,QHeaderView
from PyQt5.QtCore import pyqtSlot, Qt

import sys

from jakosc_prodDodaj import MainWindow_jakosc_prodDodaj
from _jakosc_prod_ui import Ui_Form
import db, dodatki
import configparser
import openpyxl

class MainWindow_jakosc(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.load_data_from_database()
        self.ui.tab_dane.itemChanged.connect(self.on_item_changed)

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            miestac_roboczy = dodatki.data_miesiac_dzis()
            select_data = "select * from jakosc_prod where miesiac = '%s';" % (miestac_roboczy)
            #select_data = "select * from kpi_mag"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            results = db.read_query(connection, select_data)

            self.ui.tab_dane.setColumnCount(6)  # Zmień na liczbę kolumn w twojej tabeli
            self.ui.tab_dane.setRowCount(0)  # Ustawienie liczby wierszy na 0
            self.ui.tab_dane.setHorizontalHeaderLabels([
                'Grupa',
                'Grupa robocza',
                'PPM',
                'Reklamacje',
                'Miesiac',
                'Data dodania'
            ])

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.ui.tab_dane.setRowCount(len(results))


            # Wypełnianie tabeli danymi
            for row_idx, row_data in enumerate(results):
                # Przechowujemy id każdego wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = QTableWidgetItem(str(value))
                    if col_idx == 2 or col_idx == 3:  # Zablokowanie edycji dla kolumny "nazwa"
                        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Ustawienie komórek jako edytowalne
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Usuwamy flagę edytowalności
                    print(row_idx, col_idx, item.text())
                    self.ui.tab_dane.setItem(row_idx, col_idx, item)

            # Przechowywanie id wierszy
            self.row_ids = [row_data[0] for row_data in results]
            print(row_data[0] for row_data in results)

        except db.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def on_item_changed(self, item):
        """Funkcja wywoływana przy każdej zmianie komórki."""
        row = item.row()
        col = item.column()
        new_value = item.text()

        # Pobranie id rekordu dla zmienionego wiersza
        record_id = self.row_ids[row]
        print('record_id:',record_id)

        # Zapis zmienionych danych do bazy
        self.update_database(record_id, col, new_value)

    def update_database(self, record_id, col, new_value):
        """Funkcja do aktualizacji konkretnej komórki w bazie danych."""
        try:
            # Mapowanie indeksu kolumny na nazwę kolumny w bazie
            column_names = ["grupa", "grupa_robocza", "ppm", "reklamacje"]
            column_name = column_names[col]

            # Aktualizacja w bazie danych
            sql_query = f"UPDATE jakosc_prod SET {column_name} = %s WHERE id = %s"
            connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
            db.execute_query_virable(connection,sql_query,(new_value, record_id))
            #self.cursor.execute(sql_query, (new_value, record_id))
            #self.db_connection.commit()
            print(f"Zaktualizowano rekord o id {record_id}, {column_name} = {new_value}")

        except db.Error as e:
            print(f"Błąd zapisu do bazy danych: {e}")

    def szablon(self):
        wb = openpyxl.Workbook()
        ws = wb.active

        headers = ["Grupa","Grupa robocza","PPM","Reklamacje"]
        ws.append(headers)

        line1 = ["lider","3011","",""]
        line2 = ["lider","3012","",""]
        line3 = ["lider","3013 + 3015","",""]
        line4 = ["lider","3014","",""]
        line5 = ["lider","3016 + 3019","",""]
        line6 = ["lider","3018","",""]
        line7 = ["lider","3031+3032","",""]
        line8 = ["lider","Montaż","",""]
        line9 = ["lider","Zakuwanie","",""]
        line10 = ["lider","Maszyny","",""]
        line11 = ["instruktor","Czaplinek","",""]
        line12 = ["instruktor","Borne","",""]

        ws.append(line1)
        ws.append(line2)
        ws.append(line3)
        ws.append(line4)
        ws.append(line5)
        ws.append(line6)
        ws.append(line7)
        ws.append(line8)
        ws.append(line9)
        ws.append(line10)
        ws.append(line11)
        ws.append(line12)


        # Ustawianie szerokości kolumn
        ws.column_dimensions['A'].width = 15  # Grupa
        ws.column_dimensions['B'].width = 15  # Grupa robocza
        ws.column_dimensions['C'].width = 10  # PPM
        ws.column_dimensions['D'].width = 7  # Reklamacje

        domyslna_nazwa = 'jakosc.xlsx'
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Zapisz plik",
            domyslna_nazwa,  # Domyślna nazwa pliku
            "Pliki Excel (*.xlsx);;Wszystkie pliki (*)",
            options=options
        )

        # Sprawdzanie, czy użytkownik wybrał plik
        if file_path:
            wb.save(file_path)
            print(f"Plik zapisano: {file_path}")
        else:
            print("Zapis pliku anulowany")

    def otworz_okno_jakosc_prodDodaj(self):
        self.okno_jakosc_prodDodaj = MainWindow_jakosc_prodDodaj()
        self.okno_jakosc_prodDodaj.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MainWindow_jakosc()
    editor.show()
    sys.exit(app.exec_())
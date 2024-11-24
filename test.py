import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class TableEditor(QWidget):
    def __init__(self):
        super().__init__()

        # Tworzenie tabeli QTableWidget z odpowiednimi nagłówkami kolumn
        self.table = QTableWidget(0, 3)  # Liczba kolumn ustawiona na 3, bez kolumny id
        self.table.setHorizontalHeaderLabels(['Nazwa', 'Ilość', 'Cena'])

        # Połączenie z bazą danych MySQL
        self.connect_to_database()

        # Załadowanie danych z bazy do QTableWidget
        self.load_data_from_database()

        # Layout i dodanie tabeli do widgetu
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Dodanie przycisku do usuwania wierszy
        self.delete_button = QPushButton("Usuń wiersz")
        self.delete_button.clicked.connect(self.delete_selected_row)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        # Nasłuchiwanie zmian w tabeli
        self.table.itemChanged.connect(self.on_item_changed)

    def connect_to_database(self):
        """Funkcja do połączenia z bazą danych MySQL."""
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="place_v2"
            )
            self.cursor = self.db_connection.cursor()
            print("Połączono z bazą danych.")
        except mysql.connector.Error as e:
            print(f"Błąd połączenia z bazą danych: {e}")

    def load_data_from_database(self):
        """Funkcja do załadowania danych z bazy do QTableWidget."""
        try:
            # Wykonanie zapytania do pobrania danych z tabeli
            self.cursor.execute("SELECT * FROM kpi_mag")
            results = self.cursor.fetchall()

            # Ustawianie liczby wierszy na podstawie danych z bazy
            self.table.setRowCount(len(results))

            # Wypełnianie tabeli danymi
            self.row_ids = []  # Lista do przechowywania ID wierszy
            for row_idx, row_data in enumerate(results):
                self.row_ids.append(row_data[0])  # Przechowywanie ID wiersza
                for col_idx, value in enumerate(row_data[1:]):  # Pomijamy id
                    item = QTableWidgetItem(str(value))
                    # Ustawianie edytowalności na podstawie kolumny
                    if col_idx == 0:  # Zablokowanie edycji dla kolumny "nazwa"
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    else:
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.table.setItem(row_idx, col_idx, item)

        except mysql.connector.Error as e:
            print(f"Błąd przy pobieraniu danych z bazy danych: {e}")

    def on_item_changed(self, item):
        """Funkcja wywoływana przy każdej zmianie komórki."""
        row = item.row()
        col = item.column()
        new_value = item.text()

        # Pobranie id rekordu dla zmienionego wiersza
        record_id = self.row_ids[row]

        # Zapis zmienionych danych do bazy
        self.update_database(record_id, col, new_value)

    def update_database(self, record_id, col, new_value):
        """Funkcja do aktualizacji konkretnej komórki w bazie danych."""
        try:
            # Mapowanie indeksu kolumny na nazwę kolumny w bazie
            column_names = ["nazwa", "ilosc", "cena"]
            column_name = column_names[col]

            # Aktualizacja w bazie danych
            sql_query = f"UPDATE produkty SET {column_name} = %s WHERE id = %s"
            self.cursor.execute(sql_query, (new_value, record_id))
            self.db_connection.commit()
            print(f"Zaktualizowano rekord o id {record_id}, {column_name} = {new_value}")

        except mysql.connector.Error as e:
            print(f"Błąd zapisu do bazy danych: {e}")

    def delete_selected_row(self):
        """Funkcja do usuwania zaznaczonego wiersza."""
        # Pobranie aktualnie wybranego wiersza
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Błąd", "Nie wybrano wiersza do usunięcia.")
            return

        # Potwierdzenie usunięcia
        reply = QMessageBox.question(self, "Usuń wiersz", "Czy na pewno chcesz usunąć wybrany wiersz?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Pobranie ID rekordu do usunięcia
            record_id = self.row_ids[row]

            try:
                # Usunięcie wiersza z bazy danych
                sql_query = "DELETE FROM produkty WHERE id = %s"
                self.cursor.execute(sql_query, (record_id,))
                self.db_connection.commit()
                print(f"Usunięto rekord o id {record_id}")

                # Usunięcie wiersza z tabeli i aktualizacja listy ID
                self.table.removeRow(row)
                del self.row_ids[row]

            except mysql.connector.Error as e:
                print(f"Błąd usuwania z bazy danych: {e}")

    def closeEvent(self, event):
        """Zamyka połączenie z bazą danych przy zamknięciu aplikacji."""
        if self.db_connection.is_connected():
            self.cursor.close()
            self.db_connection.close()
            print("Połączenie z bazą danych zostało zamknięte.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TableEditor()
    editor.show()
    sys.exit(app.exec_())

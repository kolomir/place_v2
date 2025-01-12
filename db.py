import mysql.connector
from mysql.connector import Error

host_name = 'localhost'
user_name = 'root'
password = ''
#database_name = 'place_v2'
#database_name = 'place_v2_test'
database_name = 'place_v2_test2'

def create_db_connection(host_name, username, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = username,
            password = user_password,
            database = db_name
        )
        print('Połączenie z bazą MySQL zostało ustanowione!')
        return connection #zwraca tylko obiekt połączenia
    except Error as err:
        print(f"Error: '{err}'")
        return None

def execute_query_virable(connection, query, virable):
    if connection is None:
        print('Nie można wykonać zapytania - brak połączenia z bazą danych')
        return
    cursor = connection.cursor()
    try:
        # query - to zapytanie wstawiające dane; variable ro dane którymi zapytanie jest wypełnione. Jest ono w formie listy
        cursor.execute(query, (virable))
        connection.commit()
        print('Query successful')
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    if connection is None:
        print('Nie można wykonać zapytania - brak połączenia z bazą danych')
        return
    cursor = connection.cursor()
    try:
        # query - to zapytanie wstawiające dane; variable ro dane którymi zapytanie jest wypełnione. Jest ono w formie listy
        cursor.execute(query)
        connection.commit()
        print('Query successful')
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
    except IndexError as err:
        print(f"Błąd indeksowania listy: {err}")
    except Exception as err:
        print(f"Nieoczekiwany błąd: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Połączenie z bazą danych zostało zamknięte.")

def pisz_error():
    return mysql.connector.Error()

# Funkcja wywołująca procedurę
def wywolaj_procedure(connection, procedure):
    cursor = connection.cursor()
    result = None

    try:
        cursor.callproc(procedure)
        rows = []
        for result in cursor.stored_results():
            rows.append(result.fetchall())
        #result = cursor.stored_results()
        return rows

        #for result in cursor.stored_results():
        #    rows = result.fetchall()
        #    for row in rows:
        #        print(row)
    except Error as err:
        print(f"Error: '{err}'")
    except IndexError as err:
        print(f"Błąd indeksowania listy: {err}")
    except Exception as err:
        print(f"Nieoczekiwany błąd: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Połączenie z bazą danych zostało zamknięte.")
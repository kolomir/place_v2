import calendar
import db, dodatki
from datetime import date, datetime

miestac_roboczy = dodatki.data_miesiac_dzis()
data = datetime.strptime(miestac_roboczy, "%Y-%m-%d")
miesiac = data.month
rok = data.year
_, dni_miesiaca = calendar.monthrange(rok, miesiac)


test = 3
def progi(wc_id):
    select_data_q_progi = "select * from progi_jakosc pj where pj.aktywny = 1 and id_ranga = 2"
    connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
    results_q_progi = db.read_query(connection, select_data_q_progi)
    connection.close()

    for dane in results_q_progi:
        if dane[2] == wc_id:
            print(dane[4],' ',dane[5],' ',dane[6])
            dol = dane[4]
            srodek = dane[5]
            gora = dane[6]
    return dol,srodek,gora

wynik = progi(test)
print('wynik0:',wynik[0])
print('wynik1:',wynik[1])
print('wynik2:',wynik[2])
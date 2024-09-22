import db, dodatki

miesiac = dodatki.data_miesiac_dzis()

select_data_bledy = "SELECT * FROM `bledy_prod` WHERE miesiac = '%s';" % (miesiac)
connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
results_bledy = db.read_query(connection, select_data_bledy)
connection.close()

szukaj = 1788
#3033
#2539
#2511
#2513
wynik = 300.00

for dane_b in results_bledy:
    wynik_b = wynik
    if szukaj == dane_b[1]:
        if dane_b[2] == 1:
            wynik_b = wynik * 0.75
            break
        if dane_b[2] == 2:
            wynik_b = wynik * 0.5
            break
        if dane_b[2] == 3:
            wynik_b = wynik * 0.25
            break
        if dane_b[2] > 3:
            wynik_b = 0
            break
print(wynik, wynik_b)



print('-------------------------------')
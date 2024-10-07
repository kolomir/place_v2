import calendar
import db, dodatki
from datetime import date, datetime

miestac_roboczy = dodatki.data_miesiac_dzis()
data = datetime.strptime(miestac_roboczy, "%Y-%m-%d")
miesiac = data.month
rok = data.year
_, dni_miesiaca = calendar.monthrange(rok, miesiac)

select_data = "SELECT * FROM `dni_pracujace_w_roku` WHERE rok = '%s' and miesiac = '%s';" % (rok,miesiac)  # (miestac_roboczy)
connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
results = db.read_query(connection, select_data)

dni_z_bazy = results[0][4]

def dni_w_miesiacach(lata):
    for miesiace in range(1, 13):
        _, dni = calendar.monthrange(lata, miesiace)
        print(f"Miesiąc {miesiace}: {dni} dni")


print('dni_z_bazy:',dni_z_bazy)
print('----------------------')
print('miesiac:',miesiac)
print('rok:',rok)
print('dni_miesiaca:',dni_miesiaca)
print('----------------------')

print('miestac_roboczy:',miestac_roboczy)

# Wywołanie dla roku 2024
dni_w_miesiacach(2024)

'''
#--------------------------------------------------------------------------------------------------------
select_data_progi = "select * from progi_prod pp where pp.id_ranga = 3 and pp.aktywny = 1"
        connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
        results_progi = db.read_query(connection, select_data_progi)
        connection.close()

        prog100 = self.ui.lab_pracujacychNieobecnosci.text()
        prog75 = self.ui.lab_pracujacych075Nieobecnosci.text()
        prog50 = self.ui.lab_pracujacych050Nieobecnosci.text()

        lista = []
        prog = 96.00
        for dane in results:
            if dane[6] > prog:
                if dane[12] > results_progi[0][6]:
                    wynik = results_progi[0][7]
                elif dane[12] > results_progi[0][4]:
                    wynik = results_progi[0][5]
                elif dane[12] > results_progi[0][2]:
                    wynik = results_progi[0][3]

                wsp = 0
                wynik_n = wynik
                suma_warunek = dane[23] + dane[24] + dane[25] + dane[26] + dane[27]
                if suma_warunek == 0:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[22])) + int(float(dane[23])) + int(
                        float(dane[24])) + int(
                        float(dane[25])) + int(float(dane[26])) + int(float(dane[27]))
                else:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[23])) + int(float(dane[24])) + int(
                        float(dane[25])) + int(
                        float(dane[26])) + int(float(dane[27]))

                if suma > int(float(prog50)):
                    wsp = 2
                    wynik_n = 0.0
                if suma <= int(float(prog50)) and suma > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
                    wynik_n = wynik / 2

                wynik_b = wynik_n
                if dane[28] == 1:
                    wynik_b = (wynik_n / 4) * 3
                if dane[28] == 2:
                    wynik_b = wynik_n / 2
                if dane[28] == 3:
                    wynik_b = wynik_n / 4
                if dane[28] > 3:
                    wynik_b = 0.0

            else:
                wynik = wynik_n = wynik_b = 0.00

                wsp = 0
                suma_warunek = dane[23] + dane[24] + dane[25] + dane[26] + dane[27]
                if suma_warunek == 0:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[22])) + int(float(dane[23])) + int(
                        float(dane[24])) + int(
                        float(dane[25])) + int(float(dane[26])) + int(float(dane[27]))
                else:
                    suma = int(float(dane[13])) + int(float(dane[14])) + int(float(dane[15])) + int(
                        float(dane[16])) + int(
                        float(dane[17])) + int(float(dane[18])) + int(float(dane[19])) + int(
                        float(dane[20])) + int(
                        float(dane[21])) + int(float(dane[23])) + int(float(dane[24])) + int(
                        float(dane[25])) + int(
                        float(dane[26])) + int(float(dane[27]))

                if suma > int(float(prog50)):
                    wsp = 2
                if suma <= int(float(prog50)) and suma > (int(float(prog100)) - int(float(prog75))):
                    wsp = 1
            #print([dane[0], dane[1], dane[2], dane[3], dane[4], dane[6], dane[8], dane[9], dane[10], dane[11], dane[12], wynik, suma, wsp, wynik_n, dane[28], wynik_b])
            lista.append([dane[0], dane[1], dane[2], dane[3], dane[4], dane[6], dane[8], dane[9], dane[10], dane[11], dane[12], wynik, suma, wsp, wynik_n, dane[28], wynik_b])
            lista.append([dane[0], dane[1], dane[2], dane[3], dane[4], dane[5], dane[6], dane[7], dane[8], dane[9], wynik, dane[10], wsp, wynik_n, dane[11], wynik_b])
'''
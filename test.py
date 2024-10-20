import calendar
import db, dodatki
from datetime import date, datetime

miestac_roboczy = dodatki.data_miesiac_dzis()
data = datetime.strptime(miestac_roboczy, "%Y-%m-%d")
miesiac = data
#miesiac = data.month
#rok = data.year
#_, dni_miesiaca = calendar.monthrange(rok, miesiac)


select_data = '''
                select 
                    d.Nr_akt 
                    ,d.dzial 
                    ,d.Direct_ 
                    ,d.Indirect_ 
                    ,ROUND(COALESCE(SUM(lz.reported), 0), 2) AS 'raportowany'
                    ,ROUND(COALESCE(SUM(lz.planned), 0), 2) AS 'planowany'
                    ,ROUND(SUM(lz.planned) / SUM(lz.reported), 2) AS 'wydajnosci'
                    ,ROUND(d.Direct_ * COALESCE(SUM(lz.planned) / NULLIF(SUM(lz.reported), 0), 0), 2) AS 'produktywnosc'
                    ,lz.zmiana 
                    ,lz.zmiana_lit 
                    ,lo.lokalizacja 
                from 
                    direct d
                        left join logowanie_zlecen lz on d.Nr_akt = lz.nr_akt 
                        left join linie l on d.dzial = l.nazwa 
                            left join lokalizacja lo on lo.id = l.id_lokalizacja 
                where 
                    d.dzial not in ('2030', '1-210', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '401', '2-305')
                    and d.miesiac = '%s'
                    and lz.miesiac = '%s'
                group by 
                    d.Nr_akt 
                    ,d.dzial 
                    ,d.Direct_work 
                    ,d.Direct_ 
                    ,d.Indirect_work
                    ,d.Indirect_ 
                ''' % (miesiac, miesiac)
connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
results = db.read_query(connection, select_data)
connection.close()

select_data_ilosc = '''
                        select 
                            l.lokalizacja , count(l.lokalizacja) 
                        from 
                            instruktor i 
                                left join linia_gniazdo lg on lg.id_lider = i.id 
                                    left join lokalizacja l on l.id = lg.id_lokalizacja 
                        where 
                            i.aktywny = 1
                            and i.id_ranga = 1
                        GROUP by 
                            l.lokalizacja 
                        '''
connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
results_ilosc = db.read_query(connection, select_data_ilosc)
connection.close()

ile_czaplinek = results_ilosc[1][1]
ile_borne = results_ilosc[0][1]

data = []
for row in results:
    data.append({
        'NrAkt': row[0],
        'dział': row[1],
        'Direct': float(row[2]),
        'Indirect': float(row[3]),
        'raportowany': float(row[4]),
        'planowany': float(row[5]),
        'wydajnosc': float(row[6]),
        'produktywnosc': float(row[7]),
        'zmiana': row[8],
        'zmianaLit': row[9],
        'lokalizacja': row[10]
    })

grouped_data = {}

for row in data:
    key = (row['lokalizacja'], row['zmianaLit'])  # Klucz to kombinacja lokalizacji i zmiany
    if key not in grouped_data:
        grouped_data[key] = {
            'Direct': 0,
            'Indirect': 0,
            'raportowany': 0,
            'planowany': 0,
            'wydajnosc': 0,
            'produktywnosc': 0
        }
        grouped_data[key]['Direct'] += row['Direct']
        grouped_data[key]['Indirect'] += row['Indirect']
        grouped_data[key]['raportowany'] += row['raportowany']
        grouped_data[key]['planowany'] += row['planowany']
        grouped_data[key]['wydajnosc'] += row['wydajnosc']
        grouped_data[key]['produktywnosc'] += row['produktywnosc']
lista = []
for key, values in grouped_data.items():
    lokalizacja, zmianaLit = key
    lista.append([lokalizacja,zmianaLit,values['Direct'],values['Indirect'],values['raportowany'],values['planowany'],values['wydajnosc'],values['produktywnosc']])

print('********************************')
print('********************************')

sum_grupy_czaplinek = {'A': [0] * 6, 'B': [0] * 6, 'C': [0] * 6}
sum_inna_czaplinek = [0] * 6
sum_grupy_borne_sulinowo = {'A': [0] * 6, 'B': [0] * 6, 'C': [0] * 6}
sum_inna_borne_sulinowo = [0] * 6

# Liczba grup w Czaplinku i Borne Sulinowo
ile_czaplinek = 2  # Zakładana wartość zmiennej, zmień ją zgodnie z potrzebą
ile_borne = 3      # Zakładana wartość zmiennej, zmień ją zgodnie z potrzebą

def dodaj_do_sumy(suma, row):
    for i in range(2, len(row)):
        suma[i-2] += row[i]

# Sumowanie z podziałem na lokalizacje i grupy
for row in data:
    if row[0] == 'Czaplinek':
        if row[1] in sum_grupy_czaplinek:
            dodaj_do_sumy(sum_grupy_czaplinek[row[1]], row)
        elif row[1] == 'inna':
            dodaj_do_sumy(sum_inna_czaplinek, row)
    elif row[0] == 'Borne Sulinowo':
        if row[1] in sum_grupy_borne_sulinowo:
            dodaj_do_sumy(sum_grupy_borne_sulinowo[row[1]], row)
        elif row[1] == 'inna':
            dodaj_do_sumy(sum_inna_borne_sulinowo, row)




print('********************************')
print('********************************')

print('miesiac:',miesiac)
print('--------------------------------')
print('test:',results)
print('--------------------------------')
print('data:',data)
print('--------------------------------')
print('lista:',lista)
print('--------------------------------')
print('results_ilosc:',results_ilosc)
print('Czaplinek:',results_ilosc[1][0],results_ilosc[1][1])
print('Borne Sulinowo:',results_ilosc[0][0],results_ilosc[0][1])
print('--------------------------------')
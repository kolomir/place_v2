import db, dodatki
import configparser
import os
import openpyxl

config = configparser.ConfigParser()
config.read('config.ini')
folder_bledy = config['sciezki']['folder_bledy']
plik = config['sciezki']['plik_raportowanie']

sciezka = "%s\\%s" % (folder_bledy,plik)

print(sciezka)

wb = openpyxl.load_workbook(os.path.join(sciezka))
sheet = wb['Sheet']

lista_wpisow = []

i = 1
for row in sheet.iter_rows(min_row=2, min_col=1, max_col=13, values_only=True):
    if any(cell is not None for cell in row):
        print(i, ' | ', row[6],' | ',row[8])
        wydajnosc = 0
        if row[6] == '' or row[6] < 0:
            print('test')
            wydajnosc = 0
        elif row[6] > 0 and row[8] == 0:
            wydajnosc = 0
        elif row[6] > 0 and row[8] == '':
            wydajnosc = 0
        elif row[6] == 0:
            wydajnosc = 0
        else:
            wydajnosc = row[6] / row[8]

        #print(i, [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], wydajnosc])
        # lista_wpisow.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],wydajnosc,data_miesiac,teraz])
        i = i + 1
    else:
        break

print('------------------------------------------------')
print('Koniec')
print('------------------------------------------------')
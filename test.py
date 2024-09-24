import os
import openpyxl
from datetime import date, datetime
import db, dodatki

plik = "D:\ProjektyPython\place_v2\\bledy\direct.xlsx"

wb = openpyxl.load_workbook(os.path.join(plik))
sheet = wb['Sheet']
teraz = datetime.today()
data_miesiac = str(dodatki.data_miesiac_dzis())
print(data_miesiac)

def czysc_string_dec(tekst):
    #wynik = tekst.replace(' ', '')
    #wynik = wynik.replace(',', '.')
    wynik = tekst.replace(',', '.')
    return wynik

lista_wpisow = []

#czytamy wszystkie kolumny i wiersze ze wskazanego pliku
for row in sheet.iter_rows(min_row=2, min_col=1, max_col=25, values_only=True):
    #sprawdzamy czy wiersz nie jest pusty (zakładając że pusty wiersz ma wszystkie kolumny o wartosci None i kończy zestawienie)
    if any(cell is not None for cell in row):
        nr_akt = int(row[0])
        dep = int(row[2])
        worked = round(row[7],2)
        direct_work = round(row[8],2)
        direct = round(row[9],2)
        indirect_work = round(row[10],2)
        indirect = round(row[11],2)
        pause = round(row[12],2)
        diff_hr = round(row[13],2)
        diff = round(row[14],2)
        #nr_akt = int(row[0])
        #dep = int(row[8])
        #worked = self.czysc_string(row[16],' hrs')
        #direct_work = self.czysc_string(row[18],' hrs')
        #direct = self.czysc_string(row[19],' %')
        #indirect_work = self.czysc_string(row[20],' hrs')
        #ndirect = self.czysc_string(row[21],' %')
        #pause = self.czysc_string(row[22],' hrs')
        #diff_hr = self.czysc_string(row[23],' hrs')
        #diff = self.czysc_string(row[24],' %')
        lista_wpisow.append([nr_akt,row[1],dep,worked,direct_work,direct,indirect_work,indirect,pause,diff_hr,diff,data_miesiac,teraz])
    else:
        break

for dane in lista_wpisow:
    print(dane)
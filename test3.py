# Przykładowe dane jako lista list
data = [
    ["403",'','','',''"MICHAŁ USZAKIEWICZ | 2899",'',''"PRACOWNIK DZIAŁU JAKOŚCI","05.09.2022",2,'','','','','','','','','','','','','','','','','','','','',2],
    ["404",'','','',''"KAROL WARACKI | 322",'',''"PRACOWNIK DZIAŁU UTRZYMANIA RUCHU","01.06.2006",'2,25','','','','','','','','','','','','','','','','','','','','','2,25'],
    ["405",'','','',''"ZBIGNIEW SKRZYPIEC | 1684",'',''"PRACOWNIK DZIAŁU UTRZYMANIA RUCHU","06.06.2011",2,'','','','','','','','','','','','','','','','','','','','',2],
    ["406",'','','',''"TOMASZ KUŹMA | 1847",'',''"PRACOWNIK DZIAŁU UTRZYMANIA RUCHU","06.03.2023",'1,1875','','','','','','','','','','','','','','','','','',1,'','','2,1875'],
    ["407",'','','',''"TOMASZ WOJTKIW | 2010",'',''"PRACOWNIK DZIAŁU UTRZYMANIA RUCHU","20.04.2015",2,'','','','','','','','','','','','','','','','','','','','',2],
    ["408",'','','',''"JACEK FLAGA | 2062",'',''"PRACOWNIK DZIAŁU UTRZYMANIA RUCHU","01.03.2016",'2,5','','','','','','','','','','','','','','','','','','','','','2,5'],
    ["409",'','','',''"MAŁGORZATA KISIEL | 1593",'',''"PRACOWNIK INWENTARYZACJI CIĄGŁEJ","27.09.2010",2,'','','','','','','','','','','','','','','','','','','','',2],
    ["448",'','','',''"AGNIESZKA GROMADA | 210",'',''"SPECJALISTA DS. BUDOWY I PROGRAMOWANIA URZĄDZEŃ TE","01.09.2005",3,'','','','','','','','','','','','','','','','','','','','',3],
    ["449",'','','',''"ADAM SZTECHMILER | 3061",'',''"SPECJALISTA DS. BUDOWY I PROGRAMOWANIA URZĄDZEŃ TESTUJĄCY","18.08.2021",'4,7188','','','','','','','','','','','','','','','','','','','','','4,7188'],
    ["450",'','','',''"PRZEMYSŁAW HANDZEL | 2868",'',''"SPECJALISTA DS. BUDOWY I PROGRAMOWANIA URZĄDZEŃ TESTUJĄCYCH","14.02.2019",8,'','','',1,'','','','','','','','','','','','','','','','',9],
    ["451",'','','',''"ANETA DRZAZGA | 2774",'',''"SPECJALISTA DS. JAKOŚCI","06.08.2018",2,'','','','','','','','','','','','','','','','','','','','',2],
    ["455",'','','',''"MATEUSZ DRAPAŁA | 2721",'',''"SPECJALISTA DS. PLANOWANIA PRODUKCJI","18.06.2018",'','','','','','','','','','','','','','','','',21,'','','','',21],
    ["456",'','','',''"EMILIA STRONA | 2945",'',''"SPECJALISTA DS. PLANOWANIA PRODUKCJI","18.01.2021",'2,625','','','','','','','','','','',3,'','','','','','','','','','5,625'],
    ["457",'','','',''"TOMASZ BIERNAT | 81",'',''"SPECJALISTA DS. SERWISU MASZYN I URZĄDZEŃ","13.09.2024",'2,25','','','','','','','','','','','','','','','','','','',1,'','3,25'],
    ["458",'','','',''"ROBERT LITWIŃCZUK | 1464",'',''"SPECJALISTA DS. ZAKUPÓW OPERACYJNYCH","22.05.2017",2,'','','','','','','','','','','','','','','','','','','','',2]
    ]

# Funkcja do zaokrąglania wartości w wierszach
def convert_and_round(value):
    if isinstance(value, str) and ',' in value:
        return round(float(value.replace(',', '.')))
    elif isinstance(value, (int, float)):
        return round(value)
    else:
        return value

# Przetwarzanie danych
for row in data:
    for i in range(len(row)):
        row[i] = convert_and_round(row[i])

# Wyświetlenie wyników
for row in data:
    print(row)
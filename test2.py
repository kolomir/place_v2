# Dane
data = [
    ['Czaplinek', 'A', 93.62, 0.93, 68.81, 72.47, 1.05, 98.6],
    ['Czaplinek', 'B', 92.24, 1.09, 100.57, 103.37, 1.03, 94.81],
    ['Borne Sulinowo', 'A', 93.44, 0.81, 119.79, 149.57, 1.25, 116.67],
    ['Czaplinek', 'inna', 93.25, 0.86, 82.5, 81.58, 0.99, 92.21],
    ['Borne Sulinowo', 'B', 91.38, 2.62, 121.38, 98.87, 0.81, 74.43],
    ['Borne Sulinowo', 'inna', 97.57, 2.4, 117.27, 112.51, 0.96, 93.61],
    ['Borne Sulinowo', 'C', 81.92, 7.97, 54.29, 50.24, 0.93, 75.81]
]

# Inicjalizacja sum dla grup
sum_grupy_czaplinek = {'A': [0] * 6, 'B': [0] * 6, 'C': [0] * 6}
sum_inna_czaplinek = [0] * 6
sum_grupy_borne_sulinowo = {'A': [0] * 6, 'B': [0] * 6, 'C': [0] * 6}
sum_inna_borne_sulinowo = [0] * 6

# Liczba grup w Czaplinku i Borne Sulinowo
ile_czaplinek = 2  # Zakładana wartość zmiennej, zmień ją zgodnie z potrzebą
ile_borne = 2      # Zakładana wartość zmiennej, zmień ją zgodnie z potrzebą

# Funkcja dodawania wartości kolumn
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

# Przypisywanie wartości z grupy 'inna' do głównych grup w Czaplinku
if ile_czaplinek == 1:
    # Suma dla wszystkich grup w Czaplinku
    for group in sum_grupy_czaplinek:
        for i in range(len(sum_grupy_czaplinek[group])):
            sum_grupy_czaplinek[group][i] += sum_inna_czaplinek[i]
elif ile_czaplinek == 2:
    # Podział grupy 'inna' na grupy A i B
    for i in range(len(sum_inna_czaplinek)):
        sum_grupy_czaplinek['A'][i] += sum_inna_czaplinek[i] / 2
        sum_grupy_czaplinek['B'][i] += sum_inna_czaplinek[i] / 2
elif ile_czaplinek == 3:
    # Podział grupy 'inna' na grupy A, B i C
    for i in range(len(sum_inna_czaplinek)):
        sum_grupy_czaplinek['A'][i] += sum_inna_czaplinek[i] / 3
        sum_grupy_czaplinek['B'][i] += sum_inna_czaplinek[i] / 3
        sum_grupy_czaplinek['C'][i] += sum_inna_czaplinek[i] / 3

# Przypisywanie wartości z grupy 'inna' do głównych grup w Borne Sulinowo
if ile_borne == 1:
    # Suma dla wszystkich grup w Borne Sulinowo
    for group in sum_grupy_borne_sulinowo:
        for i in range(len(sum_grupy_borne_sulinowo[group])):
            sum_grupy_borne_sulinowo[group][i] += sum_inna_borne_sulinowo[i]
elif ile_borne == 2:
    # Podział grupy 'inna' na grupy A i B
    for i in range(len(sum_inna_borne_sulinowo)):
        sum_grupy_borne_sulinowo['A'][i] += sum_inna_borne_sulinowo[i] / 2
        sum_grupy_borne_sulinowo['B'][i] += sum_inna_borne_sulinowo[i] / 2
elif ile_borne == 3:
    # Podział grupy 'inna' na grupy A, B i C
    for i in range(len(sum_inna_borne_sulinowo)):
        sum_grupy_borne_sulinowo['A'][i] += sum_inna_borne_sulinowo[i] / 3
        sum_grupy_borne_sulinowo['B'][i] += sum_inna_borne_sulinowo[i] / 3
        sum_grupy_borne_sulinowo['C'][i] += sum_inna_borne_sulinowo[i] / 3

# Wyświetlanie wyników
print("Suma dla Czaplinka (A):", sum_grupy_czaplinek['A'])
print("Suma dla Czaplinka (B):", sum_grupy_czaplinek['B'])
if ile_czaplinek == 3:
    print("Suma dla Czaplinka (C):", sum_grupy_czaplinek['C'])

print("Suma dla Borne Sulinowo (A):", sum_grupy_borne_sulinowo['A'])
print("Suma dla Borne Sulinowo (B):", sum_grupy_borne_sulinowo['B'])
if ile_borne == 3:
    print("Suma dla Borne Sulinowo (C):", sum_grupy_borne_sulinowo['C'])
from datetime import datetime, timedelta

# Aktualna data
#dzisiaj = datetime.now()
dzisiaj = datetime.strptime("2025-1-27", "%Y-%m-%d")

# Obliczenie przesuniętego miesiąca i roku
miesiac = dzisiaj.month - 1
rok = dzisiaj.year

# Obsługa zmiany roku, jeśli przesunięcie powoduje przejście do stycznia
if miesiac < 1:
    miesiac = 12
    rok -= 1

# Tworzenie nowej daty z przesuniętym miesiącem
przesunieta_data = dzisiaj.replace(year=rok, month=miesiac)

# Wyświetlenie roku
print("Dziś:", dzisiaj)
print("Rok po przesunięciu o jeden miesiąc:", przesunieta_data.year)
print("Miesiac po przesunięciu:", przesunieta_data.month)
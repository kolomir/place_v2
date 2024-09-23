krotka_wierszy = (
    ("Produkt 1", 100),
    ("Produkt 2", 200),
    ("Produkt 3", 300),
    ("Produkt 4", 150),
    ("Produkt 5", 120),
    ("Produkt 6", 180),
    ("Produkt 7", 0),
    ("Produkt 8", 60),
    ("Produkt 9", 110),
    ("Produkt 10", 140),
    ("Produkt 10", 0.00),
    ("Produkt 10", 140.02),
    ("Produkt 10", 140.45),
)

# Sumowanie kwot (zakładam, że kwota jest w drugim elemencie każdej krotki)
suma_kwot = sum(wiersz[1] for wiersz in krotka_wierszy)

print("Suma kwot:", suma_kwot)
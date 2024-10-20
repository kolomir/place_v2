def czas_na_dziesietny(czas):
    # Rozdzielamy godziny i minuty
    godziny, minuty = map(int, czas.split(":"))

    # Zamieniamy minuty na część dziesiętną
    dziesietny_czas = godziny + minuty / 60

    return dziesietny_czas


# Przykłady użycia:
print(czas_na_dziesietny("1:30"))  # Wyjście: 1.5
print(czas_na_dziesietny("1:45"))  # Wyjście: 1.75
print(czas_na_dziesietny("1:48"))  # Wyjście: 1.8

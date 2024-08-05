from datetime import date

nazwy_miesiecy = [
    "styczeń",
    "luty",
    "marzec",
    "kwiecień",
    "maj",
    "czerwiec",
    "lipiec",
    "sierpień",
    "wrzesień",
    "październik",
    "listopad",
    "grudzień"
]


def data_miesiac_dzis():
    data_dzis = date.today()
    prev_miesiac = data_dzis.month - 1 if data_dzis.month > 1 else 12
    prev_rok = data_dzis.year if data_dzis.month > 1 else data_dzis.year - 1
    data_miesiac = "%s-%s-%s" % (prev_rok, prev_miesiac, "1")
    print(data_miesiac)
    return data_miesiac
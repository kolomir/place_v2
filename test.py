import db, dodatki

dane = "2024-12-01"
grupa = 5

connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
#results = db.wywolaj_procedure(connection, 'PracownicyWydajnoscProduktywnosc')
#results = db.wywolaj_procedure(connection, 'PierwszyDzienNaVarchar')
#results = db.wywolaj_procedure(connection, 'PracownicyMiesiac')
#results = db.wywolaj_procedure_zmeinna(connection, 'PracownicyMiesiac', dane)

# ---- Działające w kodzie ----------------------
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_iw', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_pracownik', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_wydajnosc', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_wydania_direct', dane)
#results = db.wywolaj_procedure_zmienna2(connection, 'wyliczenia_mag_pracownik', dane, grupa)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_pracownicy_produktywnosc', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_wsparcie_produktywnosc', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_wsparcie_pracownik', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_liderzy_produktywnosc', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_liderzy_pracownik', dane)
results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_instruktorzy_produktywnosc', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_prod_instruktorzy_pracownik', dane)

#print(results)

# ---- wycofane ----------------------
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_przyjecia_pracownik', dane)
#results = db.wywolaj_procedure_zmienna(connection, 'wyliczenia_mag_transport_bs_pracownik', dane)

for data in results:
    print(data)

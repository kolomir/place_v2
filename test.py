import db, dodatki

connection = db.create_db_connection(db.host_name, db.user_name, db.password, db.database_name)
#results = db.wywolaj_procedure(connection, 'PracownicyWydajnoscProduktywnosc')
#results = db.wywolaj_procedure(connection, 'PierwszyDzienNaVarchar')
results = db.wywolaj_procedure(connection, 'PracownicyMiesiac')

#print(results)

for data in results:
    print(data)

import mysql.connector

user = input("mysql> Entrez votre utilisateur MySQL (par défaut root): ") or 'root'
password = input("mysql> Entrez votre mot de passe MySQL (par défaut root): ") or 'root'
host = input("mysql> Entrez l'hôte MySQL (par défaut localhost): ") or 'localhost'
port = input("mysql> Entrez le port MySQL (par défaut 8889): ") or 8889

database = None
config = {
    'user': user,
    'password': password,
    'host': host,
    'port': port
}

def mysql_client(query):
    global database

    try:
        connection = mysql.connector.connect(**config)

        if database:
            cursor = connection.cursor()
            cursor.execute(f"USE {database}")

        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        header = [i[0] for i in cursor.description]

        if not rows:
            print("Aucune donnée à afficher.")
            return

        max_lengths = [max(len(str(header[i])), max(len(str(row[i])) for row in rows)) + 2 for i in range(len(header))]

        separator = '+'.join('-' * length for length in max_lengths)
        print(f" {separator} ")

        header_line = '|'.join(f"{col:<{length}}" for col, length in zip(header, max_lengths))
        print(f" {header_line} ")

        print(f" {separator} ")

        for row in rows:
            row_line = '|'.join(f"{str(cell):<{length}}" for cell, length in zip(row, max_lengths))
            print(f" {row_line} ")

        print(f" {separator} ")

        print(f"mysql> Connexion réussie: {database}")

    except mysql.connector.Error as err:
        print(f"mysql> Erreur MySQL: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

while True:
    query = input("mysql> ")

    if query.lower().startswith('use'):
        parts = query.split()
        if len(parts) == 2:
            database = parts[1]
            print(f"mysql> Changement de la base de données en cours: {database}")
        else:
            print("mysql> La syntaxe correcte pour 'USE DATABASE' est 'USE nom_de_la_base'.")
        continue
    
    if query.lower() in ['exit', 'exit;']:
        print("mysql> Bye !")
        break
    else:
        mysql_client(query)
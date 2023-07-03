import mysql.connector
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = cnx.cursor()
cursor.execute("CREATE DATABASE ERP")
cnx.database = "ERP"
cursor.execute("""
    CREATE TABLE nombre_de_la_tabla (
        columna1 TIPO_DE_DATO,
        columna2 TIPO_DE_DATO,
        ...
    )
""")
# Cierra el cursor y la conexión
cursor.close()
cnx.close()

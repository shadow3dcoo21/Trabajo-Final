import tkinter as tk
from tkinter import ttk
import mysql.connector


class MySQLConnector:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from MySQL")

    def execute_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except mysql.connector.Error as error:
            print("Error executing query:", error)


class ERPApp:
    def __init__(self, root, db_connector):
        self.root = root
        self.root.title("ERP App")
        self.db_connector = db_connector

        # Crear las tablas en la base de datos
        self.create_tables()

        # Variables de productos
        self.producto_nombre = tk.StringVar()
        self.producto_cantidad = tk.StringVar()

        # Variables de finanzas
        self.finanzas_nombre = tk.StringVar()
        self.finanzas_monto = tk.StringVar()

        # Variables de personal
        self.personal_nombre = tk.StringVar()
        self.personal_accion = tk.StringVar()

        # Crear pestañas
        self.tab_control = ttk.Notebook(self.root)
        self.inventario_tab = tk.Frame(self.tab_control)
        self.finanzas_tab = tk.Frame(self.tab_control)
        self.personal_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.inventario_tab, text='Inventario')
        self.tab_control.add(self.finanzas_tab, text='Finanzas')
        self.tab_control.add(self.personal_tab, text='Personal')
        self.tab_control.pack(expand=1, fill='both')

        # Pestaña de Inventario
        self.inventario_label = tk.Label(self.inventario_tab, text='Registrar Producto')
        self.inventario_label.pack()

        self.nombre_label = tk.Label(self.inventario_tab, text='Nombre:')
        self.nombre_label.pack()
        self.nombre_entry = tk.Entry(self.inventario_tab, textvariable=self.producto_nombre)
        self.nombre_entry.pack()

        self.cantidad_label = tk.Label(self.inventario_tab, text='Cantidad:')
        self.cantidad_label.pack()
        self.cantidad_entry = tk.Entry(self.inventario_tab, textvariable=self.producto_cantidad)
        self.cantidad_entry.pack()

        self.registrar_producto_btn = tk.Button(self.inventario_tab, text='Registrar', command=self.registrar_producto)
        self.registrar_producto_btn.pack()

        # Pestaña de Finanzas
        self.finanzas_label = tk.Label(self.finanzas_tab, text='Registrar Gasto/Ingreso')
        self.finanzas_label.pack()

        self.finanzas_nombre_label = tk.Label(self.finanzas_tab, text='Concepto:')
        self.finanzas_nombre_label.pack()
        self.finanzas_nombre_entry = tk.Entry(self.finanzas_tab, textvariable=self.finanzas_nombre)
        self.finanzas_nombre_entry.pack()

        self.finanzas_monto_label = tk.Label(self.finanzas_tab, text='Monto:')
        self.finanzas_monto_label.pack()
        self.finanzas_monto_entry = tk.Entry(self.finanzas_tab, textvariable=self.finanzas_monto)
        self.finanzas_monto_entry.pack()

        self.registrar_finanzas_btn = tk.Button(self.finanzas_tab, text='Registrar', command=self.registrar_finanzas)
        self.registrar_finanzas_btn.pack()

        # Pestaña de Personal
        self.personal_label = tk.Label(self.personal_tab, text='Registrar Entrada/Salida')
        self.personal_label.pack()

        self.personal_nombre_label = tk.Label(self.personal_tab, text='Nombre:')
        self.personal_nombre_label.pack()
        self.personal_nombre_entry = tk.Entry(self.personal_tab, textvariable=self.personal_nombre)
        self.personal_nombre_entry.pack()

        self.personal_accion_label = tk.Label(self.personal_tab, text='Acción (Entrada/Salida):')
        self.personal_accion_label.pack()
        self.personal_accion_entry = tk.Entry(self.personal_tab, textvariable=self.personal_accion)
        self.personal_accion_entry.pack()

        self.registrar_personal_btn = tk.Button(self.personal_tab, text='Registrar', command=self.registrar_personal)
        self.registrar_personal_btn.pack()

    def create_tables(self):
        # Crear la tabla de productos
        query_productos = """
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            cantidad INT
        )
        """
        self.db_connector.execute_query(query_productos)

        # Crear la tabla de finanzas
        query_finanzas = """
        CREATE TABLE IF NOT EXISTS finanzas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            monto DECIMAL(10, 2)
        )
        """
        self.db_connector.execute_query(query_finanzas)

        # Crear la tabla de personal
        query_personal = """
        CREATE TABLE IF NOT EXISTS personal (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255),
            accion VARCHAR(20)
        )
        """
        self.db_connector.execute_query(query_personal)

    def registrar_producto(self):
        nombre = self.producto_nombre.get()
        cantidad = self.producto_cantidad.get()

        query = "INSERT INTO productos (nombre, cantidad) VALUES (%s, %s)"
        values = (nombre, cantidad)
        self.db_connector.execute_query(query, values)

        self.producto_nombre.set('')
        self.producto_cantidad.set('')

    def registrar_finanzas(self):
        nombre = self.finanzas_nombre.get()
        monto = self.finanzas_monto.get()

        query = "INSERT INTO finanzas (nombre, monto) VALUES (%s, %s)"
        values = (nombre, monto)
        self.db_connector.execute_query(query, values)

        self.finanzas_nombre.set('')
        self.finanzas_monto.set('')

    def registrar_personal(self):
        nombre = self.personal_nombre.get()
        accion = self.personal_accion.get()

        query = "INSERT INTO personal (nombre, accion) VALUES (%s, %s)"
        values = (nombre, accion)
        self.db_connector.execute_query(query, values)

        self.personal_nombre.set('')
        self.personal_accion.set('')


# Conexión a la base de datos
db_connector = MySQLConnector(host="localhost", username="root", password="", database="ERP")
db_connector.connect()

# Creación de la base de datos y tablas
db_connector.execute_query("CREATE DATABASE IF NOT EXISTS ERP")
db_connector.execute_query("USE ERP")

# Creación de las tablas
erp_app = tk.Tk()
app = ERPApp(erp_app, db_connector)

erp_app.mainloop()

# Cerrar la conexión a la base de datos
db_connector.disconnect()

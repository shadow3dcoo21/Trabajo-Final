import tkinter as tk
from tkinter import ttk
import mysql.connector

class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, node, key, data):
        if key < node.key:
            if node.left is None:
                node.left = Node(key, data)
            else:
                self._insert_recursive(node.left, key, data)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, data)
            else:
                self._insert_recursive(node.right, key, data)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)


class MySQLConnector:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.product_tree = BinarySearchTree()
        self.finanzas_tree = BinarySearchTree()
        self.personal_tree = BinarySearchTree()

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

    def build_trees(self):
        query_productos = "SELECT * FROM productos"
        productos = self.execute_select_query(query_productos)
        for producto in productos:
            self.product_tree.insert(producto[1], producto)

        query_finanzas = "SELECT * FROM finanzas"
        finanzas = self.execute_select_query(query_finanzas)
        for finanza in finanzas:
            self.finanzas_tree.insert(finanza[1], finanza)

        query_personal = "SELECT * FROM personal"
        personal = self.execute_select_query(query_personal)
        for persona in personal:
            self.personal_tree.insert(persona[1], persona)

    def execute_select_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print("Error executing query:", error)


class ERPApp:
    def __init__(self, root, db_connector):
        self.root = root
        self.root.title("ERP App")
        self.db_connector = db_connector

        # Crear las tablas en la base de datos
        self.create_tables()

        # Construir los árboles de búsqueda
        self.db_connector.build_trees()

        # Variables de búsqueda
        self.busqueda = tk.StringVar()

        # Crear pestañas
        self.tab_control = ttk.Notebook(self.root)
        self.inventario_tab = tk.Frame(self.tab_control)
        self.finanzas_tab = tk.Frame(self.tab_control)
        self.personal_tab = tk.Frame(self.tab_control)
        self.busqueda_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.inventario_tab, text='Inventario')
        self.tab_control.add(self.finanzas_tab, text='Finanzas')
        self.tab_control.add(self.personal_tab, text='Personal')
        self.tab_control.add(self.busqueda_tab, text='Búsqueda')
        self.tab_control.pack(expand=1, fill='both')

        # Pestaña de Inventario
        self.inventario_label = tk.Label(self.inventario_tab, text='Registrar Producto')
        self.inventario_label.pack()

        # ...

        # Pestaña de Finanzas
        self.finanzas_label = tk.Label(self.finanzas_tab, text='Registrar Gasto/Ingreso')
        self.finanzas_label.pack()

        # ...

        # Pestaña de Personal
        self.personal_label = tk.Label(self.personal_tab, text='Registrar Entrada/Salida')
        self.personal_label.pack()

        # ...

        # Pestaña de Búsqueda
        self.busqueda_label = tk.Label(self.busqueda_tab, text='Buscar:')
        self.busqueda_label.pack()
        self.busqueda_entry = tk.Entry(self.busqueda_tab, textvariable=self.busqueda)
        self.busqueda_entry.pack()

        self.buscar_btn = tk.Button(self.busqueda_tab, text='Buscar', command=self.buscar)
        self.buscar_btn.pack()

        self.resultados_text = tk.Text(self.busqueda_tab, height=10, width=50)
        self.resultados_text.pack()

    def buscar(self):
        busqueda = self.busqueda.get()

        # Buscar en el árbol de productos
        resultados_productos = self.db_connector.product_tree.search(busqueda)

        # Buscar en el árbol de finanzas
        resultados_finanzas = self.db_connector.finanzas_tree.search(busqueda)

        # Buscar en el árbol de personal
        resultados_personal = self.db_connector.personal_tree.search(busqueda)

        # Mostrar los resultados en el widget de texto
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, "Resultados de la búsqueda:\n\n")

        self.resultados_text.insert(tk.END, "Productos:\n")
        if resultados_productos:
            self.resultados_text.insert(tk.END, f"ID: {resultados_productos.data[0]}, Nombre: {resultados_productos.data[1]}, Cantidad: {resultados_productos.data[2]}\n")

        self.resultados_text.insert(tk.END, "\nFinanzas:\n")
        if resultados_finanzas:
            self.resultados_text.insert(tk.END, f"ID: {resultados_finanzas.data[0]}, Concepto: {resultados_finanzas.data[1]}, Monto: {resultados_finanzas.data[2]}\n")

        self.resultados_text.insert(tk.END, "\nPersonal:\n")
        if resultados_personal:
            self.resultados_text.insert(tk.END, f"ID: {resultados_personal.data[0]}, Nombre: {resultados_personal.data[1]}, Acción: {resultados_personal.data[2]}\n")


# Resto del código no modificado

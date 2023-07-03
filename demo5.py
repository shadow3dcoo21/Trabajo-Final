import tkinter as tk
from tkinter import ttk
import mysql.connector


class BinarySearchTree:
    class Node:
        def __init__(self, key, data):
            self.key = key
            self.data = data
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if not self.root:
            self.root = self.Node(key, data)
        else:
            self._insert_recursively(self.root, key, data)

    def _insert_recursively(self, node, key, data):
        if key < node.key:
            if node.left:
                self._insert_recursively(node.left, key, data)
            else:
                node.left = self.Node(key, data)
        elif key > node.key:
            if node.right:
                self._insert_recursively(node.right, key, data)
            else:
                node.right = self.Node(key, data)

    def search(self, key):
        return self._search_recursively(self.root, key)

    def _search_recursively(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search_recursively(node.left, key)
        return self._search_recursively(node.right, key)


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
            print("Base de datos Deconectada")

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

    def execute_select_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Error executing query:", error)
            return []

    def build_trees(self):
        # Construir el árbol de productos
        query_productos = "SELECT * FROM productos"
        resultados_productos = self.execute_select_query(query_productos)
        for producto in resultados_productos:
            self.product_tree.insert(producto[1], producto)

        # Construir el árbol de finanzas
        query_finanzas = "SELECT * FROM finanzas"
        resultados_finanzas = self.execute_select_query(query_finanzas)
        for finanza in resultados_finanzas:
            self.finanzas_tree.insert(finanza[1], finanza)

        # Construir el árbol de personal
        query_personal = "SELECT * FROM personal"
        resultados_personal = self.execute_select_query(query_personal)
        for persona in resultados_personal:
            self.personal_tree.insert(persona[1], persona)


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

        # Pestaña de Búsqueda
        #self.busqueda_tab = tk.Frame(self.tab_control)
        #self.tab_control.add(self.busqueda_tab, text='Búsqueda')
        #self.tab_control.pack(expand=1, fill='both')

        #self.busqueda_label = tk.Label(self.busqueda_tab, text='Buscar en la base de datos')
        #self.busqueda_label.pack()

        #self.busqueda_entry = tk.Entry(self.busqueda_tab)
        #self.busqueda_entry.pack()

        #self.busqueda_btn = tk.Button(self.busqueda_tab, text='Buscar', command=self.buscar)
        #self.busqueda_btn.pack()

        #self.resultados_text = tk.Text(self.busqueda_tab, height=10, width=50)
        #self.resultados_text.pack()

        # Pestaña de Búsqueda con árbol binario de búsqueda
        self.busqueda_tree_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.busqueda_tree_tab, text='Búscar')
        self.tab_control.pack(expand=1, fill='both')

        self.busqueda_tree_label = tk.Label(self.busqueda_tree_tab, text='Buscar en la base de datos (Árbol)')
        self.busqueda_tree_label.pack()

        self.busqueda_tree_entry = tk.Entry(self.busqueda_tree_tab)
        self.busqueda_tree_entry.pack()

        self.busqueda_tree_btn = tk.Button(self.busqueda_tree_tab, text='Buscar', command=self.buscar_arbol)
        self.busqueda_tree_btn.pack()

        self.resultados_tree = ttk.Treeview(self.busqueda_tree_tab, columns=('ID', 'Nombre', 'Cantidad', 'Concepto', 'Monto', 'Acción'))
        self.resultados_tree.heading('#0', text='Tipo')
        self.resultados_tree.heading('ID', text='ID')
        self.resultados_tree.heading('Nombre', text='Nombre')
        self.resultados_tree.heading('Cantidad', text='Cantidad')
        self.resultados_tree.heading('Concepto', text='Concepto')
        self.resultados_tree.heading('Monto', text='Monto')
        self.resultados_tree.heading('Acción', text='Acción')
        self.resultados_tree.pack()

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

    def registrar_finanzas(self):
        nombre = self.finanzas_nombre.get()
        monto = self.finanzas_monto.get()

        query = "INSERT INTO finanzas (nombre, monto) VALUES (%s, %s)"
        values = (nombre, monto)
        self.db_connector.execute_query(query, values)

    def registrar_personal(self):
        nombre = self.personal_nombre.get()
        accion = self.personal_accion.get()

        query = "INSERT INTO personal (nombre, accion) VALUES (%s, %s)"
        values = (nombre, accion)
        self.db_connector.execute_query(query, values)

    def buscar(self):
        query = self.busqueda_entry.get()
        resultados = self.db_connector.execute_select_query(query)

        self.resultados_text.delete('1#', tk.END)
        for resultado in resultados:
            self.resultados_text.insert(tk.END, str(resultado) + '\n')

    def buscar_arbol(self):
        query = self.busqueda_tree_entry.get()
        resultado_productos = self.db_connector.product_tree.search(query)
        resultado_finanzas = self.db_connector.finanzas_tree.search(query)
        resultado_personal = self.db_connector.personal_tree.search(query)

        self.resultados_tree.delete(*self.resultados_tree.get_children())
        if resultado_productos:
            self.resultados_tree.insert('', tk.END, text='Producto', values=resultado_productos.data)
        if resultado_finanzas:
            self.resultados_tree.insert('', tk.END, text='Finanza', values=resultado_finanzas.data)
        if resultado_personal:
            self.resultados_tree.insert('', tk.END, text='Personal', values=resultado_personal.data)


if __name__ == '__main__':
    db_connector = MySQLConnector('localhost', 'root', '', 'ERP')
    db_connector.connect()
    db_connector.build_trees()

    root = tk.Tk()
    app = ERPApp(root, db_connector)
    root.mainloop()

    db_connector.disconnect()

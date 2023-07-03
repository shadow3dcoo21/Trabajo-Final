import tkinter as tk
from tkinter import ttk


class ERPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ERP App")

        # Variables de productos
        self.productos = []
        self.producto_nombre = tk.StringVar()
        self.producto_cantidad = tk.StringVar()

        # Variables de finanzas
        self.total_ventas = 0
        self.total_gastos = 0

        # Variables de personal
        self.personal_entrada = []
        self.personal_salida = []
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

        self.registrar_btn = tk.Button(self.inventario_tab, text='Registrar', command=self.registrar_producto)
        self.registrar_btn.pack()

        # Pestaña de Finanzas
        self.finanzas_label = tk.Label(self.finanzas_tab, text='Gestión de Finanzas')
        self.finanzas_label.pack()

        self.ventas_label = tk.Label(self.finanzas_tab, text=f'Total Ventas: {self.total_ventas}')
        self.ventas_label.pack()

        self.gastos_label = tk.Label(self.finanzas_tab, text=f'Total Gastos: {self.total_gastos}')
        self.gastos_label.pack()

        # Pestaña de Personal
        self.personal_label = tk.Label(self.personal_tab, text='Registrar Entrada/Salida de Personal')
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

    def registrar_producto(self):
        nombre = self.producto_nombre.get()
        cantidad = self.producto_cantidad.get()
        self.productos.append({'nombre': nombre, 'cantidad': cantidad})

        self.producto_nombre.set('')
        self.producto_cantidad.set('')

        print('Producto registrado:', nombre, cantidad)

    def registrar_personal(self):
        nombre = self.personal_nombre.get()
        accion = self.personal_accion.get()

        if accion.lower() == 'entrada':
            self.personal_entrada.append(nombre)
        elif accion.lower() == 'salida':
            self.personal_salida.append(nombre)

        self.personal_nombre.set('')
        self.personal_accion.set('')

        print('Registro de personal:', nombre, accion)


root = tk.Tk()
app = ERPApp(root)
root.mainloop()

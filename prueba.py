import matplotlib.pyplot as plt

# Definir los nombres de los paquetes
paquetes = ['Enfermeria', 'Pacientes', 'Medicamentos', 'Agenda', 'Reportes']

# Definir las dependencias entre los paquetes
dependencias = {
    'Enfermeria': [],
    'Pacientes': ['Enfermeria'],
    'Medicamentos': ['Enfermeria'],
    'Agenda': ['Enfermeria', 'Pacientes'],
    'Reportes': ['Enfermeria', 'Pacientes', 'Medicamentos']
}

# Crear el gráfico de paquetes
fig, ax = plt.subplots()

# Dibujar los paquetes
ax.broken_barh([(0, 1)], (10, 10), facecolors='blue', edgecolor='black', label='Enfermeria')
ax.broken_barh([(0, 1)], (30, 10), facecolors='green', edgecolor='black', label='Pacientes')
ax.broken_barh([(0, 1)], (50, 10), facecolors='orange', edgecolor='black', label='Medicamentos')
ax.broken_barh([(0, 1)], (70, 10), facecolors='purple', edgecolor='black', label='Agenda')
ax.broken_barh([(0, 1)], (90, 10), facecolors='red', edgecolor='black', label='Reportes')

# Dibujar las dependencias
for paquete, dependencias_paquete in dependencias.items():
    y_start = 15 + paquetes.index(paquete) * 20
    for dependencia in dependencias_paquete:
        y_end = 15 + paquetes.index(dependencia) * 20 + 5
        ax.arrow(1.1, y_start, 3, y_end - y_start, head_width=1, head_length=2, fc='black', ec='black')

# Configurar el gráfico
ax.set_ylim(0, len(paquetes) * 20 + 20)
ax.set_xlim(0, 10)
ax.set_xlabel('Paquetes')
ax.set_yticks([25 + i * 20 for i in range(len(paquetes))])
ax.set_yticklabels(paquetes)
ax.legend(loc='upper right')
ax.set_title('Diagrama de Paquetes')

# Mostrar el gráfico
plt.show()

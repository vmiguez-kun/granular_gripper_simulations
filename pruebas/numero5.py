import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------- PARÁMETROS DE CONTROL ----------
inicio = 0    # Índice relativo en la lista de tipo 1 (ej: del 10 al 50 entre los tipo 1)
fin = 6932
magnificacion_pos = 10
escala_vector = 0.05

# ---------- Archivos de entrada ----------
archivo_atoms = "atoms_tipo1_2.txt"
archivo_normales = "normal_vectors2.txt"

# ---------- Cargar coordenadas de tipo 1 ----------
coordenadas_tipo1 = []
with open(archivo_atoms, "r") as f_atoms:
    for linea in f_atoms:
        partes = linea.strip().split()
        if len(partes) >= 5 and partes[1] == "1":  # solo tipo 1
            try:
                x = float(partes[2]) * magnificacion_pos
                y = float(partes[3]) * magnificacion_pos
                z = float(partes[4]) * magnificacion_pos
                coordenadas_tipo1.append((x, y, z))
            except ValueError:
                continue

# ---------- Cargar vectores normales ----------
vectores_normales = []
with open(archivo_normales, "r") as f_normales:
    for linea in f_normales:
        linea = linea.strip()
        if linea.startswith("[") and linea.endswith("]"):
            try:
                vector = eval(linea)
                if isinstance(vector, list) and len(vector) == 3:
                    vectores_normales.append(np.array(vector) * escala_vector)
            except:
                continue

# ---------- Validación ----------
if len(vectores_normales) != len(coordenadas_tipo1):
    print("❌ ERROR: Cantidad de vectores y coordenadas tipo 1 no coinciden.")
    print(f"Vectores normales: {len(vectores_normales)}")
    print(f"Coordenadas tipo 1: {len(coordenadas_tipo1)}")
    exit()

# ---------- Preparar datos del rango ----------
X, Y, Z = [], [], []
U, V, W = [], [], []

for idx in range(inicio - 1, fin):  # índice relativo
    if 0 <= idx < len(coordenadas_tipo1):
        x, y, z = coordenadas_tipo1[idx]
        u, v, w = vectores_normales[idx]
        X.append(x)
        Y.append(y)
        Z.append(z)
        U.append(u)
        V.append(v)
        W.append(w)

# ---------- Graficar ----------
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')

ax.quiver(X, Y, Z, U, V, W, color='red', arrow_length_ratio=0.1)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Vectores normales de tipo 1 desde índice {inicio} hasta {fin} (×{magnificacion_pos})')

ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-3, 5])
ax.view_init(elev=10, azim=30)

plt.tight_layout()
plt.show()

#visualización de los normal vectors en cada coordenada correspondiente a donde se aplica
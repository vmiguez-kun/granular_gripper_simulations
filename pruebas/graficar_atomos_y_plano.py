import numpy as np
import matplotlib.pyplot as plt

# ------------------ PARÁMETROS EDITABLES ------------------
ids_a_graficar = []
planos_a_graficar = [203,246,248,249,250]
archivo_atoms = "atoms_tipo1_2.txt"
archivo_planos = "planos.txt"
archivo_ecuaciones = "ec_plano.txt"

# ------------------ CARGAR COORDENADAS DE ÁTOMOS ------------------
coordenadas = {}
with open(archivo_atoms, "r") as f:
    for linea in f:
        partes = linea.strip().split()
        if len(partes) >= 5:
            try:
                id_atom = int(partes[0])
                x, y, z = map(float, partes[2:5])
                coordenadas[id_atom] = (x, y, z)
            except:
                continue

# ------------------ CARGAR TODOS LOS PLANOS ------------------
planos_dict = {}
plano_actual = None
with open(archivo_planos, "r") as f:
    for linea in f:
        linea = linea.strip()
        if linea.startswith("plano"):
            plano_actual = int(linea.split()[1])
            planos_dict[plano_actual] = []
        elif plano_actual is not None and linea:
            try:
                ids = list(map(int, linea.split()))
                planos_dict[plano_actual].extend(ids)
            except:
                continue

# ------------------ CARGAR ECUACIONES DE PLANOS DESDE ARCHIVO ------------------
ecuaciones = {}
with open(archivo_ecuaciones, "r") as f:
    lineas = f.readlines()

i = 0
while i < len(lineas):
    linea = lineas[i].strip()
    if linea.startswith("ecuacion del plano"):
        try:
            n_plano = int(linea.split()[-1])
            coefs_line = lineas[i + 1].strip()
            # Parsear A, B, C, D desde la línea
            coefs = coefs_line.replace("x", "").replace("y", "").replace("z", "").replace("=", "").replace("+", " +").split()
            A = float(coefs[0])
            B = float(coefs[2])
            C = float(coefs[4])
            D = float(coefs[6])
            ecuaciones[n_plano] = (A, B, C, D)
        except:
            pass
    i += 1

# ------------------ GRAFICAR ------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar átomos seleccionados
for atom_id in ids_a_graficar:
    if atom_id in coordenadas:
        x, y, z = coordenadas[atom_id]
        ax.scatter(x, y, z, color='red')
        ax.text(x, y, z, f'{atom_id}', fontsize=9)

# Graficar planos seleccionados
for plano_id in planos_a_graficar:
    ids = planos_dict.get(plano_id, [])
    puntos_plano = [coordenadas[i] for i in ids if i in coordenadas]

    if not puntos_plano:
        print(f"⚠️ No se encontraron puntos para el plano {plano_id}")
        continue

    puntos_plano = np.array(puntos_plano)
    ax.scatter(puntos_plano[:, 0], puntos_plano[:, 1], puntos_plano[:, 2],
               label=f"Puntos plano {plano_id}", alpha=0.4)

    # Usar coeficientes desde ec_plano.txt
    if plano_id not in ecuaciones:
        print(f"⚠️ No se encontró ecuación para el plano {plano_id}")
        continue

    A, B, C, D = ecuaciones[plano_id]
    centroide = np.mean(puntos_plano, axis=0)

    # Crear malla de plano
    xx, yy = np.meshgrid(
        np.linspace(centroide[0] - 0.01, centroide[0] + 0.01, 10),
        np.linspace(centroide[1] - 0.01, centroide[1] + 0.01, 10)
    )
    zz = (-A * xx - B * yy - D) / C

    ax.plot_surface(xx, yy, zz, alpha=0.3, label=f"Plano {plano_id}", color=np.random.rand(3,))

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title(f"Átomos {ids_a_graficar} y planos {planos_a_graficar}")
plt.legend()
plt.tight_layout()
plt.show()

#como lo dice su nombre, toma los ids del plano, toma el plano, y grafica ambos. 
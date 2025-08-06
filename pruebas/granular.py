import numpy as np
from scipy.spatial import cKDTree

# Parámetros
R = 0.065             # Radio de la semiesfera y cilindro
H = 0.16             # Altura del cilindro superior
n_semi = 6000        # Número de partículas en la semiesfera
n_cil = 9000         # Número de partículas en el cilindro
min_dist = 0.004     # Distancia mínima entre partículas
atom_type = 4

coords = []

# Generadores
def generar_en_semiesfera():
    while True:
        x = np.random.uniform(-R, R)
        y = np.random.uniform(-R, R)
        z = np.random.uniform(-R, 0)
        if x**2 + y**2 + z**2 < R**2:
            return [x, y, z]

def generar_en_cilindro():
    while True:
        x = np.random.uniform(-R, R)
        y = np.random.uniform(-R, R)
        if x**2 + y**2 < R**2:
            z = np.random.uniform(0.0, H)
            return [x, y, z]

# Árbol de vecinos
tree = cKDTree(np.empty((0, 3)))
intentos = 0
max_intentos = 1_000_000

# ---------------------
# Generar semiesfera
# ---------------------
count_semi = 0
while count_semi < n_semi and intentos < max_intentos:
    nueva = generar_en_semiesfera()
    if len(coords) > 0:
        dist, _ = tree.query(nueva, k=1)
        if dist < min_dist:
            intentos += 1
            continue
    coords.append(nueva)
    count_semi += 1
    tree = cKDTree(np.array(coords))
    intentos += 1

print(intentos)
# ---------------------
# Generar cilindro
# ---------------------
count_cil = 0
while count_cil < n_cil and intentos < max_intentos:
    nueva = generar_en_cilindro()
    if len(coords) > 0:
        dist, _ = tree.query(nueva, k=1)
        if dist < min_dist:
            intentos += 1
            continue
    coords.append(nueva)
    count_cil += 1
    tree = cKDTree(np.array(coords))
    intentos += 1
print(intentos)
# ---------------------
# Resultado
# ---------------------
esperadas = n_semi + n_cil
total = len(coords)

if total < esperadas:
    print(f"⚠️ Se generaron {total} partículas de {esperadas} esperadas tras {intentos} intentos.")
else:
    print(f"✅ Se generaron exactamente {total} partículas sin superposición.")

# Guardar archivo
with open("granular.data", "w") as f:
    for i, (x, y, z) in enumerate(coords, start=7134):
        f.write(f"{i} {atom_type} {x:.6f} {y:.6f} {z:.6f} 0.004 1000 0\n")

print("📄 Archivo 'granular.data' guardado correctamente.")

import numpy as np

# ---------- PARÁMETROS ----------
archivo_atoms = "atoms_tipo1_2.txt"
archivo_normales = "normal_vectors.txt"
archivo_salida = "aplicar_fuerzas_por_region.in"

radio_region = 0.002
magnitud_fuerza = 0.00005

# ---------- LEER COORDENADAS DE ÁTOMOS TIPO 1 ----------
coordenadas_tipo1 = []

with open(archivo_atoms, "r") as f_atoms:
    for linea in f_atoms:
        partes = linea.strip().split()
        if len(partes) >= 5:
            id_atom = int(partes[0])
            tipo = int(partes[1])
            if tipo == 1:
                x, y, z = map(float, partes[2:5])
                coordenadas_tipo1.append((id_atom, x, y, z))

print(f"✅ Se encontraron {len(coordenadas_tipo1)} partículas de tipo 1.")

# ---------- LEER VECTORES NORMALES ----------
vectores_normales = []
with open(archivo_normales, "r") as f_normales:
    for linea in f_normales:
        linea = linea.strip()
        if linea.startswith("[") and linea.endswith("]"):
            try:
                vector = eval(linea)
                if isinstance(vector, list) and len(vector) == 3:
                    vectores_normales.append(np.array(vector))
            except:
                continue

print(f"✅ Se encontraron {len(vectores_normales)} vectores normales.")

if len(coordenadas_tipo1) != len(vectores_normales):
    print("❌ ERROR: Cantidad de coordenadas y vectores no coincide.")
    exit()

# ---------- ESCRIBIR ARCHIVO DE SALIDA ----------
with open(archivo_salida, "w") as out:
    out.write("# Regiones y fix addforce sin usar group\n\n")

    for (atom_id, x, y, z), normal in zip(coordenadas_tipo1, vectores_normales):
        fx, fy, fz = magnitud_fuerza * normal
        region_id = f"reg{atom_id}"
        fix_id = f"f{atom_id}"

        out.write(f"region {region_id} sphere {x:.6f} {y:.6f} {z:.6f} {radio_region} units box\n")
        out.write(f"fix {fix_id} all addforce {fx:.6e} {fy:.6e} {fz:.6e} region {region_id}\n\n")

print(f"✅ Archivo '{archivo_salida}' generado con {len(coordenadas_tipo1)} regiones y fixes sin usar groups.")

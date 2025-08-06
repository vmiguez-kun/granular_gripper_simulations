import os
import numpy as np

# ========================
# CONFIGURACIÓN DE ARCHIVOS
# ========================

# Entrada inicial
ARCHIVO_ENTRADA_LAMMPS = "sistema_vacio1.data"

# Intermedios
ARCHIVO_POST_COORDS = "coords_vacio1.data"
ARCHIVO_ATOMS_TIPO1_2 = "atoms_tipo1_2_vacio1.txt"
ARCHIVO_BONDS_POR_ATOM = "bonds_per_atom.txt"
ARCHIVO_PLANOS = "planos.txt"
ARCHIVO_ATOMS_POR_PLANO = "atoms_por_plano_vacio1.txt"
ARCHIVO_VECTORES_NORMALES = "normal_vectors_vacio1.txt"
ARCHIVO_EC_PLANOS = "ec_plano_vacio1.txt"

# Salida final
ARCHIVO_FUERZAS = "fuerzas1.in"

# ========================
# FUNCIONES
# ========================

def leer_atoms_ordenados(lineas):
    atoms = []
    for i, linea in enumerate(lineas):
        if linea.strip() == "Atoms":
            inicio = i + 2
            break
    else:
        raise ValueError("No se encontró la sección 'Atoms'.")
    
    for linea in lineas[inicio:]:
        if linea.strip() == "" or not linea[0].isdigit():
            break
        datos = linea.strip().split()
        atoms.append((int(datos[0]), datos[:-2]))
    atoms.sort(key=lambda x: x[0])
    return [dato for _, dato in atoms], inicio + len(atoms)

def leer_bonds(lineas, desde_indice):
    for i in range(desde_indice, len(lineas)):
        if lineas[i].strip() == "Bonds":
            inicio = i + 2
            break
    else:
        return []
    
    bonds = []
    for linea in lineas[inicio:]:
        if linea.strip() == "" or not linea[0].isdigit():
            break
        bonds.append(linea.strip().split())
    return bonds

def guardar_salida(atoms, bonds, archivo_salida):
    encabezado = """LAMMPS data file via semiesfera generator

22133 atoms
14264 bonds
5 atom types
1 bond types

-0.2000 0.2000 xlo xhi
-0.2000 0.2000 ylo yhi
-0.3000 0.5000 zlo zhi

Atoms

"""
    with open(archivo_salida, 'w') as f:
        f.write(encabezado)
        for linea in atoms:
            f.write(" ".join(linea) + "\n")
        if bonds:
            f.write("\nBonds\n\n")
            for bond in bonds:
                f.write(" ".join(bond) + "\n")

def filtrar_atoms_tipo1_y_2(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as f:
        lineas = f.readlines()
    for i, linea in enumerate(lineas):
        if linea.strip() == "Atoms":
            inicio = i + 1
            break
    else:
        raise ValueError("No se encontró sección 'Atoms'.")
    
    atoms = []
    for linea in lineas[inicio:]:
        if linea.strip() == "Bonds":
            break
        if linea.strip():
            cols = linea.strip().split()
            if cols[1] in ("1", "2"):
                atoms.append((int(cols[0]), cols))
    atoms.sort()
    with open(archivo_salida, 'w') as f:
        for _, cols in atoms:
            f.write(" ".join(cols) + "\n")

def generar_bonds_por_atomo_tipo1(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as f:
        lineas = f.readlines()
    atom_ids = []
    for i, linea in enumerate(lineas):
        if linea.strip() == "Atoms":
            inicio_atoms = i + 1
            break
    else:
        raise ValueError("No se encontró sección 'Atoms'.")
    i = inicio_atoms
    while i < len(lineas) and lineas[i].strip() == "":
        i += 1
    while i < len(lineas) and lineas[i].strip():
        partes = lineas[i].strip().split()
        if partes[1] == "1":
            atom_ids.append(partes[0])
        i += 1
    for i, linea in enumerate(lineas):
        if linea.strip() == "Bonds":
            inicio_bonds = i + 2
            break
    else:
        return
    bonds = [l.strip().split() for l in lineas[inicio_bonds:] if l.strip()]
    with open(archivo_salida, 'w') as f:
        for aid in atom_ids:
            relacionados = [b for b in bonds if b[2] == aid or b[3] == aid]
            if relacionados:
                f.write(f"atom {aid}\n")
                for b in relacionados:
                    f.write(" ".join(b) + "\n")
                f.write("\n")

def generar_planos_desde_bonds(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as f:
        lineas = f.readlines()
    planos = []
    ids = set()
    actual = None
    for linea in lineas:
        if linea.startswith("atom"):
            if actual:
                planos.append((actual, sorted(ids, key=int)))
            actual = linea.replace("atom", "plano").strip()
            ids = set()
        elif linea.strip():
            ids.update([linea.split()[2], linea.split()[3]])
    if actual:
        planos.append((actual, sorted(ids, key=int)))
    with open(archivo_salida, 'w') as f:
        for nombre, ids in planos:
            f.write(f"{nombre}\n\n{' '.join(ids)}\n\n")

def extraer_atoms_por_plano(planos_file, coords_file, salida_file, total_planos):
    with open(planos_file) as f: planos = f.readlines()
    d = {}
    actual = None
    for l in planos:
        if l.startswith("plano"):
            actual = l.strip()
            d[actual] = []
        elif actual and l.strip():
            d[actual].extend(l.strip().split())
    with open(coords_file) as f: coords = f.readlines()
    for i, l in enumerate(coords):
        if l.strip() == "Atoms":
            inicio = i + 2
            break
    for j in range(inicio, len(coords)):
        if coords[j].strip() in ["", "Velocities", "Bonds"]:
            fin = j
            break
    else: fin = len(coords)
    dic_atoms = {l.split()[0]: l.strip() for l in coords[inicio:fin]}
    with open(salida_file, 'w') as f:
        for i in range(1, total_planos+1):
            clave = f"plano {i}"
            if clave in d:
                f.write(f"{clave}\n\n")
                for aid in d[clave]:
                    if aid in dic_atoms:
                        f.write(dic_atoms[aid] + "\n")
                f.write("\n")

def ajustar_plano_por_regresion(puntos):
    puntos = np.array(puntos)
    A_mat = np.column_stack((puntos[:, 0], puntos[:, 1], np.ones_like(puntos[:, 0])))
    coef, _, _, _ = np.linalg.lstsq(A_mat, puntos[:, 2], rcond=None)
    A, B, C, D = coef[0], coef[1], -1.0, coef[2]
    normal = np.array([A, B, C])
    normal /= np.linalg.norm(normal)
    centroide = puntos.mean(axis=0)
    if np.dot(normal, -centroide) < 0:
        normal *= -1
        A, B, C, D = -A, -B, -C, -D
    return A, B, C, D, normal

def calcular_vectores_normales(archivo_atoms_por_plano, archivo_normales, archivo_ec):
    with open(archivo_atoms_por_plano) as f:
        lineas = f.readlines()
    puntos = []
    actual = None
    with open(archivo_normales, 'w') as out_n, open(archivo_ec, 'w') as out_ec:
        for l in lineas:
            if l.startswith("plano "):
                if puntos:
                    A, B, C, D, normal = ajustar_plano_por_regresion(puntos)
                    out_n.write(f"vector normal del {actual}\n{normal.tolist()}\n\n")
                    out_ec.write(f"ecuacion del {actual}\n{A:.6f} x + {B:.6f} y + {C:.6f} z + {D:.6f} = 0\n\n")
                actual = l.strip()
                puntos = []
            elif l.strip():
                partes = l.strip().split()
                puntos.append(list(map(float, partes[2:5])))
        if puntos:
            A, B, C, D, normal = ajustar_plano_por_regresion(puntos)
            out_n.write(f"vector normal del {actual}\n{normal.tolist()}\n")
            out_ec.write(f"ecuacion del {actual}\n{A:.6f} x + {B:.6f} y + {C:.6f} z + {D:.6f} = 0\n")

def generar_fuerzas(archivo_atoms, archivo_normales, archivo_salida, radio_region=0.002, magnitud_fuerza=0.00005):
    coords = []
    with open(archivo_atoms) as f:
        for l in f:
            cols = l.strip().split()
            if cols[1] == "1":
                coords.append((int(cols[0]), float(cols[2]), float(cols[3]), float(cols[4])))
    normales = []
    with open(archivo_normales) as f:
        for l in f:
            if l.startswith("["):
                normales.append(np.array(eval(l.strip())))
    if len(coords) != len(normales):
        print("❌ ERROR: coordenadas y normales no coinciden.")
        return
    with open(archivo_salida, 'w') as f:
        for (aid, x, y, z), n in zip(coords, normales):
            fx, fy, fz = magnitud_fuerza * n
            f.write(f"region reg{aid} sphere {x:.6f} {y:.6f} {z:.6f} {radio_region} units box\n")
            f.write(f"fix f{aid} all addforce {fx:.6e} {fy:.6e} {fz:.6e} region reg{aid}\n\n")

# ========================
# EJECUCIÓN
# ========================
def main():
    if not os.path.isfile(ARCHIVO_ENTRADA_LAMMPS):
        print(f"❌ No se encontró {ARCHIVO_ENTRADA_LAMMPS}")
        return
    
    with open(ARCHIVO_ENTRADA_LAMMPS) as f:
        lineas = f.readlines()

    atoms, idx = leer_atoms_ordenados(lineas)
    bonds = leer_bonds(lineas, idx)
    guardar_salida(atoms, bonds, ARCHIVO_POST_COORDS)
    filtrar_atoms_tipo1_y_2(ARCHIVO_POST_COORDS, ARCHIVO_ATOMS_TIPO1_2)
    generar_bonds_por_atomo_tipo1(ARCHIVO_POST_COORDS, ARCHIVO_BONDS_POR_ATOM)
    generar_planos_desde_bonds(ARCHIVO_BONDS_POR_ATOM, ARCHIVO_PLANOS)
    extraer_atoms_por_plano(ARCHIVO_PLANOS, ARCHIVO_POST_COORDS, ARCHIVO_ATOMS_POR_PLANO, total_planos=7133)
    calcular_vectores_normales(ARCHIVO_ATOMS_POR_PLANO, ARCHIVO_VECTORES_NORMALES, ARCHIVO_EC_PLANOS)
    generar_fuerzas(ARCHIVO_ATOMS_TIPO1_2, ARCHIVO_VECTORES_NORMALES, ARCHIVO_FUERZAS)

if __name__ == "__main__":
    main()

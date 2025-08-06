import os

def leer_atoms_ordenados(lineas):
    atoms = []
    atoms_encontrado = False

    for i, linea in enumerate(lineas):
        if linea.strip() == "Atoms":
            atoms_encontrado = True
            indice_inicio = i + 2
            break

    if not atoms_encontrado:
        raise ValueError("No se encontró la sección 'Atoms'.")

    for linea in lineas[indice_inicio:]:
        if linea.strip() == "" or not linea[0].isdigit():
            break
        datos = linea.strip().split()
        id_particula = int(datos[0])
        datos = datos[:-2]  # Quitar las dos últimas columnas
        atoms.append((id_particula, datos))

    atoms.sort(key=lambda x: x[0])
    return [dato for _, dato in atoms], indice_inicio + len(atoms)

def leer_bonds(lineas, desde_indice):
    bonds = []
    bonds_encontrado = False

    for i in range(desde_indice, len(lineas)):
        if lineas[i].strip() == "Bonds":
            bonds_encontrado = True
            indice_inicio = i + 2
            break

    if not bonds_encontrado:
        return []

    for linea in lineas[indice_inicio:]:
        if linea.strip() == "" or not linea[0].isdigit():
            break
        datos = linea.strip().split()
        bonds.append(datos)

    return bonds

def guardar_salida(atoms_ordenados, bonds, nombre_salida):
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
    with open(nombre_salida, 'w') as salida:
        salida.write(encabezado)
        for linea in atoms_ordenados:
            salida.write(" ".join(linea) + "\n")

        if bonds:
            salida.write("\nBonds\n\n")
            for bond in bonds:
                salida.write(" ".join(bond) + "\n")

def filtrar_atoms_tipo1_y_2(nombre_archivo_entrada, nombre_archivo_salida):
    try:
        with open(nombre_archivo_entrada, 'r') as f:
            lineas = f.readlines()

        atoms_filtrados = []
        atoms_encontrado = False

        for i, linea in enumerate(lineas):
            if linea.strip() == "Atoms":
                atoms_encontrado = True
                indice_inicio = i + 1
                break

        if not atoms_encontrado:
            raise ValueError("No se encontró la sección 'Atoms' en el archivo.")

        for linea in lineas[indice_inicio:]:
            if linea.strip() == "":
                continue
            if linea.strip() == "Bonds":
                break
            columnas = linea.strip().split()
            tipo = columnas[1]
            if tipo in ("1", "2"):
                id_particula = int(columnas[0])
                atoms_filtrados.append((id_particula, columnas))

        atoms_filtrados.sort(key=lambda x: x[0])

        with open(nombre_archivo_salida, 'w') as f:
            for _, columnas in atoms_filtrados:
                f.write(" ".join(columnas) + "\n")

        print(f"✅ Archivo con átomos tipo 1 y 2 guardado como '{nombre_archivo_salida}'.")
    except Exception as e:
        print(f"❌ Error al filtrar átomos tipo 1 y 2: {e}")

def main():
    nombre_archivo = "sistema_final.data"   #acá va el archivo de entrada. ALSDJAKJSDoasIDJoisdj

    if not os.path.isfile(nombre_archivo):
        print(f"❌ El archivo '{nombre_archivo}' no existe.")
        return

    try:
        with open(nombre_archivo, 'r') as f:
            lineas = f.readlines()

        atoms_ordenados, indice_despues_atoms = leer_atoms_ordenados(lineas)
        bonds = leer_bonds(lineas, indice_despues_atoms)
        nombre_salida = "post_coords.data"                        #acá va el nombre de salidaaaaa ALKDJSl
        guardar_salida(atoms_ordenados, bonds, nombre_salida)

        # NUEVO BLOQUE: filtrar tipo 1 y 2 desde archivo generado
        filtrar_atoms_tipo1_y_2(nombre_salida, "atoms_tipo1_2.txt")

        print(f"\n✅ Archivo '{nombre_salida}' creado con Atoms ordenados (sin las últimas 2 columnas) y Bonds copiados.")
    except Exception as e:
        print(f"❌ Error: {e}")
        

if __name__ == "__main__":
    main()

#ESTE ARCHIVO CREA UN NUEVO DATAFILE INPUT PARA LIGGGHTS, Y TAMBIÉN EXTRAE LOS ATOMS 1Y2 EN OTRO ARCHIVO


def generar_bonds_por_atomo_tipo1(archivo_entrada, archivo_salida):
    try:
        with open(archivo_entrada, 'r') as f:
            lineas = f.readlines()

        # ---------- Buscar sección Atoms ----------
        atom_ids_tipo1 = []
        start_atoms = None
        for i, linea in enumerate(lineas):
            if linea.strip() == "Atoms":
                start_atoms = i + 1
                break

        if start_atoms is None:
            print("❌ No se encontró la sección 'Atoms'.")
            return

        # Saltar líneas vacías y leer átomos
        i = start_atoms
        while i < len(lineas) and lineas[i].strip() == "":
            i += 1

        while i < len(lineas) and lineas[i].strip() != "":
            partes = lineas[i].strip().split()
            if len(partes) >= 2:
                atom_id = partes[0]
                atom_type = partes[1]
                if atom_type == "1":
                    atom_ids_tipo1.append(atom_id)
            i += 1

        if not atom_ids_tipo1:
            print("⚠️ No se encontraron átomos de tipo 1.")
            return

        # ---------- Buscar sección Bonds ----------
        start_bonds = None
        for i, linea in enumerate(lineas):
            if linea.strip() == "Bonds":
                start_bonds = i + 2  # Saltar línea vacía
                break

        if start_bonds is None:
            print("❌ No se encontró la sección 'Bonds'.")
            return

        bonds_lines = []
        for linea in lineas[start_bonds:]:
            if linea.strip() == "":
                continue
            partes = linea.strip().split()
            if len(partes) < 4:
                continue
            bonds_lines.append(partes)

        # ---------- Escribir salida ----------
        with open(archivo_salida, 'w') as f_out:
            count = 0
            for atom_id in atom_ids_tipo1:
                bonds_atom = [bond for bond in bonds_lines if bond[2] == atom_id or bond[3] == atom_id]
                if bonds_atom:
                    f_out.write(f"atom {atom_id}\n")
                    for bond in bonds_atom:
                        f_out.write(" ".join(bond) + "\n")
                    f_out.write("\n")
                    count += 1

        print(f"✅ Se escribieron {count} secciones de bonds (solo átomos tipo 1).")
        print(f"📄 Archivo generado: '{archivo_salida}'")

    except Exception as e:
        print(f"❌ Error: {e}")


generar_bonds_por_atomo_tipo1("post_coords.data", "bonds_per_atom.txt")


#ESTE PROGRAMA CREA SECCIONES DONDE TENEMOS LOS ENLACES QUE TIENE CADA ATOMO de tipo 1.

def generar_planos_desde_bonds(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            lineas = f.readlines()

        planos = []
        current_atom = None
        current_ids = set()

        for linea in lineas:
            linea = linea.strip()
            if linea == "":
                continue

            if linea.startswith("atom"):
                if current_atom is not None:
                    planos.append((current_atom, sorted(current_ids, key=int)))
                current_atom = linea.replace("atom", "plano").strip()
                current_ids = set()
            else:
                partes = linea.split()
                if len(partes) >= 4:
                    current_ids.add(partes[2])  # tercer columna
                    current_ids.add(partes[3])  # cuarta columna

        # No olvidar el último plano
        if current_atom is not None:
            planos.append((current_atom, sorted(current_ids, key=int)))

        # Escribir archivo de salida
        with open(output_file, 'w') as f_out:
            for nombre_plano, ids in planos:
                f_out.write(f"{nombre_plano}\n\n")
                f_out.write(" ".join(ids) + "\n\n")

        print(f"✅ Archivo '{output_file}' generado correctamente.")

    except Exception as e:
        print(f"❌ Error: {e}")


# USO
generar_planos_desde_bonds("bonds_per_atom.txt", "planos.txt")

#ESTE PROGRAMA EXTRAE LOS IDS DE LAS PARTICULAS DE CADA PLANO A PARTIR DEL BONDS PER ATOM


def extraer_atoms_por_plano(planos_file, coords_file, salida_file, total_planos=7133):
    try:
        # Paso 1: leer todos los planos
        with open(planos_file, 'r') as f:
            lineas_planos = f.readlines()

        planos = {}
        plano_actual = None

        for linea in lineas_planos:
            linea_strip = linea.strip()
            if linea_strip.startswith("plano"):
                plano_actual = linea_strip
                planos[plano_actual] = []
            elif plano_actual and linea_strip:
                planos[plano_actual].extend(linea_strip.split())

        # Paso 2: leer la sección Atoms de post_coords.txt
        with open(coords_file, 'r') as f:
            lineas_coords = f.readlines()

        atoms_start = None
        atoms_end = None

        for i, linea in enumerate(lineas_coords):
            if linea.strip() == "Atoms":
                atoms_start = i + 2  # Saltar línea vacía después de 'Atoms'
                break

        if atoms_start is None:
            print("❌ No se encontró la sección 'Atoms' en el archivo.")
            return

        for j in range(atoms_start, len(lineas_coords)):
            if lineas_coords[j].strip() in ["Velocities", "Bonds", ""]:
                atoms_end = j
                break

        if atoms_end is None:
            atoms_end = len(lineas_coords)

        # Cargar todas las líneas de Atoms en un diccionario por ID
        atoms_dict = {}
        for linea in lineas_coords[atoms_start:atoms_end]:
            columnas = linea.strip().split()
            if len(columnas) >= 1:
                atom_id = columnas[0]
                atoms_dict[atom_id] = linea.strip()

        # Paso 3: recorrer todos los planos y escribir el archivo de salida
        with open(salida_file, 'w') as f_out:
            for i in range(1, total_planos + 1):
                nombre_plano = f"plano {i}"
                if nombre_plano in planos:
                    ids_plano = planos[nombre_plano]
                    f_out.write(f"{nombre_plano}\n\n")
                    for atom_id in ids_plano:
                        if atom_id in atoms_dict:
                            f_out.write(atoms_dict[atom_id] + "\n")
                    f_out.write("\n")  # Separador entre planos

        print(f"✅ Archivo '{salida_file}' generado correctamente.")

    except Exception as e:
        print(f"❌ Error: {e}")

# USO
extraer_atoms_por_plano("planos.txt", "post_coords.data", "atoms_por_plano.txt", total_planos=7133)

#ESTE PROGRAMA AGARRA LOS IDS DE LAS PARTICULAS DE CADA PLANO, Y EXTRAE LAS COORDENADAS DE LOS MISMOS. 


import numpy as np

def ajustar_plano_por_regresion(puntos):
    """
    Ajusta un plano z = ax + by + c a un conjunto de puntos,
    y devuelve su forma general Ax + By + Cz + D = 0 y el vector normal.
    """
    puntos = np.array(puntos)
    X = puntos[:, 0]
    Y = puntos[:, 1]
    Z = puntos[:, 2]

    A_mat = np.column_stack((X, Y, np.ones_like(X)))
    coef, _, _, _ = np.linalg.lstsq(A_mat, Z, rcond=None)

    a, b, c = coef
    A = a
    B = b
    C = -1.0
    D = c

    normal = np.array([A, B, C])
    normal /= np.linalg.norm(normal)

    centroide = np.mean(puntos, axis=0)
    if np.dot(normal, -centroide) < 0:
        normal = -normal
        A, B, C = -A, -B, -C
        D = -D

    return A, B, C, D, normal

# ----------- PARTE PRINCIPAL -----------
archivo = "atoms_por_plano.txt"
salida_vectores = "normal_vectors.txt"
salida_ecuaciones = "ec_plano.txt"

with open(archivo, "r") as f:
    lineas = f.readlines()

with open(salida_vectores, "w") as out_vec, open(salida_ecuaciones, "w") as out_eq:
    plano_actual = None
    puntos = []

    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("plano "):
            if puntos:
                A, B, C, D, normal = ajustar_plano_por_regresion(puntos)

                # Guardar vector normal
                out_vec.write(f"vector normal del {plano_actual}\n")
                out_vec.write(f"{normal.tolist()}\n\n")

                # Guardar ecuación del plano
                out_eq.write(f"ecuacion del {plano_actual}\n")
                out_eq.write(f"{A:.6f} x + {B:.6f} y + {C:.6f} z + {D:.6f} = 0\n\n")

            plano_actual = linea
            puntos = []
        elif linea:
            partes = linea.split()
            if len(partes) >= 5:
                try:
                    x, y, z = map(float, partes[2:5])
                    puntos.append([x, y, z])
                except ValueError:
                    continue

    # Último plano
    if puntos:
        A, B, C, D, normal = ajustar_plano_por_regresion(puntos)

        out_vec.write(f"vector normal del {plano_actual}\n")
        out_vec.write(f"{normal.tolist()}\n")

        out_eq.write(f"ecuacion del {plano_actual}\n")
        out_eq.write(f"{A:.6f} x + {B:.6f} y + {C:.6f} z + {D:.6f} = 0\n")


#este programa calcula a partir de las coordenadas de los ids de los atomos de cada plano, un vector normal
#tiene como salida un archivo normal_vectors.txt
#Primero crea la ecuación del plano y luego calcula el vector normal. 


import numpy as np

# ---------- PARÁMETROS ----------
archivo_atoms = "atoms_tipo1_2.txt"
archivo_normales = "normal_vectors.txt"
archivo_salida = "fuerzas.in"

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

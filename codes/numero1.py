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
    nombre_archivo = "coords.data"

    if not os.path.isfile(nombre_archivo):
        print(f"❌ El archivo '{nombre_archivo}' no existe.")
        return

    try:
        with open(nombre_archivo, 'r') as f:
            lineas = f.readlines()

        atoms_ordenados, indice_despues_atoms = leer_atoms_ordenados(lineas)
        bonds = leer_bonds(lineas, indice_despues_atoms)
        nombre_salida = "post_coords.data"
        guardar_salida(atoms_ordenados, bonds, nombre_salida)

        # NUEVO BLOQUE: filtrar tipo 1 y 2 desde archivo generado
        filtrar_atoms_tipo1_y_2(nombre_salida, "atoms_tipo1_2.txt")

        print(f"\n✅ Archivo '{nombre_salida}' creado con Atoms ordenados (sin las últimas 2 columnas) y Bonds copiados.")
    except Exception as e:
        print(f"❌ Error: {e}")
        

if __name__ == "__main__":
    main()

#ESTE ARCHIVO CREA UN NUEVO DATAFILE INPUT PARA LIGGGHTS, Y TAMBIÉN EXTRAE LOS ATOMS 1Y2 EN OTRO ARCHIVO
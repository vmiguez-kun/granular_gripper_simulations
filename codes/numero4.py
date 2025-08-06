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
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
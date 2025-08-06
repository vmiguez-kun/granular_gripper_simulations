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
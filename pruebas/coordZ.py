def extraer_coordZ_y_movimiento(input_file='coords_relajado.data', output_file='coordZ.txt',
                                 z_offset=0.1, distancia=0.1, velocidad=0.625, dt=4e-6):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Detectar sección ATOMS
    atom_header = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("item: atoms"):
            atom_header = line.strip().split()[2:]  # ['id', 'type', 'x', 'y', 'z']
            atom_lines = lines[i+1:]
            break
        elif line.strip().lower() == "atoms":
            atom_header = ['id', 'type', 'x', 'y', 'z']  # Asumido por defecto
            atom_lines = lines[i+1:]
            break
    else:
        raise ValueError("No se encontró sección de átomos.")

    try:
        id_index = atom_header.index('id')
        z_index = atom_header.index('z')
    except ValueError:
        raise ValueError("No se encontró 'id' o 'z' en el encabezado de átomos.")

    # Buscar partícula con ID 1
    coordZ = None
    for line in atom_lines:
        if not line.strip() or line.strip().startswith('#'):
            continue
        parts = line.strip().split()
        if parts[id_index] == '1':
            coordZ = float(parts[z_index])
            break

    if coordZ is None:
        raise ValueError("No se encontró la partícula con ID 1.")

    coordZ_modificada = coordZ + z_offset

    # Calcular movimiento
    movetime = distancia / velocidad

    with open(output_file, 'w') as f_out:
        f_out.write(f"variable coordZ equal {coordZ_modificada:.6f}\n")
        f_out.write(f"\n#Variables de movimiento del objeto\n")
        f_out.write(f"variable movevelZ equal {velocidad:.6f} #velocidad de movimiento\n")
        f_out.write(f"variable movetimeZ equal {movetime:.6f}\n")
        f_out.write(f"variable movestepsZ equal ${{movetimeZ}}/${{dt}} #40000 dt=({dt})\n")

    print(f"Coordenada Z modificada: {coordZ_modificada:.6f}")
    print(f"Tiempo de movimiento: {movetime:.6f} s")
    print(f"Todo guardado en '{output_file}'")

# Ejecutar
if __name__ == '__main__':
    extraer_coordZ_y_movimiento()

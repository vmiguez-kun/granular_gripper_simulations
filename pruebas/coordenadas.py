#Acá es para un mallado en una semiesfera


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parámetros
R = 0.07          # Radio de la semiesfera
n_z = 55     # Número de niveles en altura (división del ángulo polar θ)
n_phi = 200       # Número de partículas por anillo (división del ángulo azimutal φ)

coords = [(0,0,-R)] #esto hace que el polo esté al principio y eso corre el indice.
                    # el primer valor del .txt tiene el polo como partícula fija, y la
                    # primer partícula con índice tipo 1 debe ser de tipo 2 para ser fija
                    #las de tipo 1 son las de la red/globo, las de tipo 2 son las fijas en el anillo superior.
                   
anillos = [[]]


# Ésta sección tiene más átomos a medida nos acercamos al polo. 

idx = 1
for i in range(n_z, 0, -1):
    theta = (i / n_z) * (np.pi / 2)
    z = R * np.cos(theta)
    r_xy = R * np.sin(theta)

    # Ajustar número de partículas por anillo según el radio actual
    n_phi_local = max(5, int(n_phi * r_xy / R+1))  # evita valores demasiado pequeños

    anillo = []
    for j in range(n_phi_local):
        phi = (j / n_phi_local) * 2 * np.pi + i * 10
        x = r_xy * np.cos(phi)
        y = r_xy * np.sin(phi)
        coords.append([x, y, -z])
        anillo.append(idx)
        idx += 1
    anillos.append(anillo)



# Convertir a numpy array
coords = np.array(coords)

# Construcción de enlaces entre vecinos del mismo anillo (cerrado)

pairs = []


for anillo in reversed(anillos):
    n = len(anillo)
    if n > 1:
        for i in range(n):
            a = anillo[i]
            b = anillo[(i + 1) % n]  # conexión circular
            pairs.append((a, b))

# Enlaces entre anillos consecutivos
for k in range(1, len(anillos) - 1):  # sin el punto solitario
    anillo_superior = anillos[k]
    anillo_inferior = anillos[k + 1]
    for a in anillo_superior:
        pos_a = coords[a]
        # buscar el más cercano en el anillo de abajo
        min_dist = float('inf')
        closest_b = None
        for b in anillo_inferior:
            pos_b = coords[b]
            dist = np.linalg.norm(pos_a - pos_b)
            if dist < min_dist:
                min_dist = dist
                closest_b = b
        pairs.append((a, closest_b))

# Conectar el polo (átomo 1, índice 0) con todos los átomos del último anillo
polo_id = 0
ultimo_anillo = anillos[-1]  # anillo más cercano al polo
for j in ultimo_anillo:
    pairs.append((polo_id, j))

 #Visualización
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], color='orange', s=20)
#ax.set_box_aspect([2, 2, 2])

for i in range(1,len(anillos)):
    print(len(anillos[i]))
print(len(coords))

# Dibujar enlaces
#for i, j in pairs:
#    xi, yi, zi = coords[i]
#    xj, yj, zj = coords[j]
#    ax.plot([xi, xj], [yi, yj], [zi, zj], 'b-', lw=0.8)

#ax.set_xlabel("X")
#ax.set_ylabel("Y")
#ax.set_zlabel("Z")
#plt.title("Mallado sobre la semiesfera con enlaces circulares por anillo")
#plt.show()

# Obtener índices del primer anillo (el más grande)
indices_top = anillos[1]

# Obtener coordenadas del primer anillo
coords_top = coords[indices_top]

# Obtener coordenadas del resto, excluyendo el punto inicial y el primer anillo
indices_rest = []
for anillo in anillos[2:]:  # omitir anillos[0] (punto solitario) y anillos[1] (top)
    indices_rest.extend(anillo)

coords_rest = coords[indices_rest]


# Guardar en archivo coords.txt
with open("coords.txt", "w") as f:
    f.write("LAMMPS data file via semiesfera generator\n\n")
    f.write(f"{len(coords)} atoms\n")
    f.write(f"{len(pairs)} bonds\n")
    f.write("5 atom types\n")  # Ahora hay tipo 1 y tipo 2
    f.write("1 bond types\n\n")
    
    xlo, xhi = -0.2, 0.2
    ylo, yhi = -0.2, 0.2
    zlo, zhi = -0.3, 0.5
    f.write(f"{xlo:.4f} {xhi:.4f} xlo xhi\n")
    f.write(f"{ylo:.4f} {yhi:.4f} ylo yhi\n")
    f.write(f"{zlo:.4f} {zhi:.4f} zlo zhi\n\n")

    f.write("Atoms\n\n")
    for i, (x, y, z) in enumerate(coords, start=1):
        atom_type = 2 if i in indices_top else 1
        f.write(f"{i} {atom_type} {x:.6f} {y:.6f} {z:.6f} 0.002 1000 0\n")

    f.write("\nBonds\n\n")
    for b_id, (i, j) in enumerate(pairs, start=1):
        f.write(f"{b_id} 1 {i+1} {j+1}\n")

print("✅ Archivo 'coords.txt' generado correctamente.")


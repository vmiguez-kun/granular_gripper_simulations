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
salida_vectores = "normal_vectors2.txt"
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
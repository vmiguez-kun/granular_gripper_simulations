import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------------
# Parámetros del campo
# -----------------------------------
Rmax = 0.1       # radio máximo
Hcampo = -0.1    # altura del cilindro (en negativo)
Fmag = 0.1       # magnitud de la fuerza total

# -----------------------------------
# Crear una malla en coordenadas cilíndricas
# -----------------------------------
n_r = 10         # puntos en el radio
n_theta = 24     # puntos angulares
n_z = 5          # puntos en Z

r = np.linspace(0.001, Rmax, n_r)
theta = np.linspace(0, 2*np.pi, n_theta)
z = np.linspace(Hcampo, 0.0, n_z)

R, Theta, Z = np.meshgrid(r, theta, z, indexing='ij')

# Convertir a coordenadas cartesianas
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# -----------------------------------
# Calcular alpha (en radianes de 0 a pi/2)
# -----------------------------------
alpha = (1 - R / Rmax) * (np.pi / 2.0)


# -----------------------------------
# Calcular componentes de fuerza
# -----------------------------------
r_safe = R + 1.0e-10
Fx = -Fmag * np.cos(alpha) * X / r_safe
Fy = -Fmag * np.cos(alpha) * Y / r_safe
Fz = Fmag * np.sin(alpha)

# -----------------------------------
# Graficar en 3D
# -----------------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, Fx, Fy, Fz, length=0.01, normalize=True, color='royalblue')

ax.set_title('Campo vectorial 3D en simetría cilíndrica')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-Rmax, Rmax)
ax.set_ylim(-Rmax, Rmax)
ax.set_zlim(Hcampo, 0.0)
ax.view_init(elev=25, azim=135)
plt.tight_layout()
plt.show()

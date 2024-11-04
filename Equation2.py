import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Coefficients of the system
A = np.array([[2, 1, -2],
              [3, 2, -4],
              [5, 4, -1]])

# Constants
B = np.array([8, 15, 1])

# Solve the system of equations
solution = np.linalg.solve(A, B)
print("Solution:", solution)

# Define the range for xi
xi = np.linspace(-5, 5, 400)

# Define the functions based on the equations
def f1(x1, x2):
    return (8 - 2*x1 - x2) / -2

def f2(x1, x2):
    return (15 - 3*x1 - 2*x2) / -4

def f3(x1, x2):
    return (1 - 5*x1 - 4*x2) / -1

# Create a meshgrid for plotting
X1, X2 = np.meshgrid(xi, xi)

# Calculate Z values for each function
Z1 = f1(X1, X2)
Z2 = f2(X1, X2)
Z3 = f3(X1, X2)

# Plot the functions in 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X1, X2, Z1, color='r', alpha=0.5, label='2x1 + x2 - 2x3 = 8')
ax.plot_surface(X1, X2, Z2, color='g', alpha=0.5, label='3x1 + 2x2 - 4x3 = 15')
ax.plot_surface(X1, X2, Z3, color='b', alpha=0.5, label='5x1 + 4x2 - x3 = 1')

ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('x3')
ax.set_title('3D Plot of the Functions')
ax.legend(['2x1 + x2 - 2x3 = 8', '3x1 + 2x2 - 4x3 = 15', '5x1 + 4x2 - x3 = 1'])

plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Coefficients of the system
A = np.array([[2, 2, -1, 1],
              [4, 3, -1, 2],
              [8, 5, -3, 4],
              [3, 3, -2, 2]])

# Constants
B = np.array([4, 6, 12, 6])

# Solve the system of equations
solution = np.linalg.solve(A, B)
print("Solution:", solution)

# Define the range for xi
xi = np.linspace(-5, 5, 400)

# Define the functions based on the equations
def f1(x1, x2, x4):
    return (4 - 2*x1 - 2*x2 + x4) / 1

def f2(x1, x2, x4):
    return (6 - 4*x1 - 3*x2 + 2*x4) / 1

def f3(x1, x2, x4):
    return (12 - 8*x1 - 5*x2 + 4*x4) / 3

def f4(x1, x2, x4):
    return (6 - 3*x1 - 3*x2 + 2*x4) / 2

# Create a meshgrid for plotting
X1, X2 = np.meshgrid(xi, xi)

# Calculate Z values for each function
Z1 = f1(X1, X2, 0)
Z2 = f2(X1, X2, 0)
Z3 = f3(X1, X2, 0)
Z4 = f4(X1, X2, 0)

# Plot the functions in 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X1, X2, Z1, color='r', alpha=0.5, label='2x1 + 2x2 - x3 + x4 = 4')
ax.plot_surface(X1, X2, Z2, color='g', alpha=0.5, label='4x1 + 3x2 - x3 + 2x4 = 6')
ax.plot_surface(X1, X2, Z3, color='b', alpha=0.5, label='8x1 + 5x2 - 3x3 + 4x4 = 12')
ax.plot_surface(X1, X2, Z4, color='y', alpha=0.5, label='3x1 + 3x2 - 2x3 + 2x4 = 6')

ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('x3')
ax.set_title('3D Plot of the Functions')
ax.legend(['2x1 + 2x2 - x3 + x4 = 4', '4x1 + 3x2 - x3 + 2x4 = 6', '8x1 + 5x2 - 3x3 + 4x4 = 12', '3x1 + 3x2 - 2x3 + 2x4 = 6'])

plt.show()

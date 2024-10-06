import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Function to create vertices of a cube
def create_cube():
    r = [-1, 1]
    vertices = np.array([[x, y, z] for x in r for y in r for z in r])
    return vertices

# Function to create edges of the cube
def create_edges(vertices):
    edges = [
        [vertices[0], vertices[1], vertices[3], vertices[2]],  # front face
        [vertices[4], vertices[5], vertices[7], vertices[6]],  # back face
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # bottom face
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # top face
        [vertices[0], vertices[2], vertices[6], vertices[4]],  # left face
        [vertices[1], vertices[3], vertices[7], vertices[5]],  # right face
    ]
    return np.array(edges)

# Function to compute depth and color of edges
def compute_depth_color(edges, ax):
    z_depth = np.mean(edges[:, :, 2], axis=1)
    colors = plt.cm.get_cmap('RdYlGn')(1 - (z_depth - z_depth.min()) / (z_depth.max() - z_depth.min()))
    return z_depth, colors

# Function to update the cube animation
def update(num, edges, poly_collection, ax):
    angle = num * np.pi / 180
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    rotated_edges = np.dot(edges.reshape(-1, 3), rotation_matrix).reshape(edges.shape)
    z_depth, colors = compute_depth_color(rotated_edges, ax)
    
    poly_collection.set_verts(rotated_edges)
    poly_collection.set_edgecolors(colors)
    
    return poly_collection,

# Setup the plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)
ax.axis('off')

# Create the cube
vertices = create_cube()
edges = create_edges(vertices)

# Create the Poly3DCollection
poly_collection = Poly3DCollection(edges, linewidths=2, edgecolors='w')
ax.add_collection3d(poly_collection)

# Set limits for the axes
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=360, fargs=(edges, poly_collection, ax), interval=20, blit=False)

# Save the animation as a gif or display it
ani.save('rotating-cube.gif', writer='imagemagick')
plt.show()

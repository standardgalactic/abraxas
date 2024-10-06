import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Function to create vertices of a cube
def create_cube():
    r = [-1, 1]
    vertices = np.array([[x, y, z] for x in r for y in r for z in r])
    return vertices

# Function to create edges of the cube
def create_edges(vertices):
    edges = [
        [vertices[0], vertices[1]], [vertices[1], vertices[3]], [vertices[3], vertices[2]], [vertices[2], vertices[0]],  # front face
        [vertices[4], vertices[5]], [vertices[5], vertices[7]], [vertices[7], vertices[6]], [vertices[6], vertices[4]],  # back face
        [vertices[0], vertices[4]], [vertices[1], vertices[5]], [vertices[2], vertices[6]], [vertices[3], vertices[7]]   # connecting edges
    ]
    return np.array(edges)

# Function to divide edges into segments
def segment_edges(edges, segments=10):
    segmented_edges = []
    for edge in edges:
        for i in range(segments):
            t = i / segments
            start = (1 - t) * edge[0] + t * edge[1]
            end = (1 - (t + 1) / segments) * edge[0] + (t + 1) / segments * edge[1]
            segmented_edges.append([start, end])
    return np.array(segmented_edges)

# Function to compute distance-based color of edges
def compute_distance_color(edges):
    distances = np.mean(np.linalg.norm(edges, axis=2), axis=1)
    norm_distances = (distances - distances.min()) / (distances.max() - distances.min())
    
    # Gradient from green (near) to yellow (mid) to amber (far)
    colors = np.zeros((len(norm_distances), 4))
    for i, distance in enumerate(norm_distances):
        if distance < 0.5:
            colors[i] = plt.colormaps['Greens'](2 * distance)  # Transition from green to yellow
        else:
            colors[i] = plt.colormaps['YlOrBr'](2 * (distance - 0.5))  # Transition from yellow to amber
    return colors

# Function to update the cube animation
def update(num, edges, line_collection, ax):
    angle = num * np.pi / 180
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    rotated_edges = np.dot(edges.reshape(-1, 3), rotation_matrix).reshape(edges.shape)
    colors = compute_distance_color(rotated_edges)
    
    line_collection.set_segments(rotated_edges)
    line_collection.set_color(colors)
    
    return line_collection,

# Setup the plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)
ax.axis('off')

# Create the cube
vertices = create_cube()
edges = create_edges(vertices)
segmented_edges = segment_edges(edges)

# Create the Line3DCollection
line_collection = Line3DCollection(segmented_edges, linewidths=2)
ax.add_collection3d(line_collection)

# Set limits for the axes
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=360, fargs=(segmented_edges, line_collection, ax), interval=20, blit=False)

# Save the animation as a gif or display it
ani.save('spin-cube.gif', writer='imagemagick')
plt.show()

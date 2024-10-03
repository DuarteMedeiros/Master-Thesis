import matplotlib.pyplot as plt
import numpy as np

def draw_regular_hexagon(center, radius):
    angles = np.linspace(0, 2*np.pi, 7)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    plt.plot(x, y, 'b-')
    # Draw line connecting the final vertex to the first vertex
    plt.plot([x[-1], x[0]], [y[-1], y[0]], 'b-')

def generate_centers(initial_center, n):
    centers = [initial_center]
    deltas = [(3/2, np.sqrt(3)/2), (3/2, -np.sqrt(3)/2), (0, -np.sqrt(3)), (-3/2, -np.sqrt(3)/2), (-3/2, np.sqrt(3)/2), (0, np.sqrt(3))]
    
    while len(centers) < n:
        new_centers = []
        for center in centers:
            for delta in deltas:
                new_center = (center[0] + delta[0], center[1] + delta[1])
                if new_center not in centers and new_center not in new_centers:
                    new_centers.append(new_center)
        centers.extend(new_centers)

    return centers

def draw_surface_with_hexagons(initial_center, n, hexagon_radius):
    centers = generate_centers(initial_center, n)
    for center in centers:
        draw_regular_hexagon(center, hexagon_radius)

    plt.axis('off')  # Remove the axes
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Example usage:
initial_center = (0, 0)  # Initial center of the surface
n = 127                   # Number of hexagons
hexagon_radius = 1       # Radius of each hexagon

draw_surface_with_hexagons(initial_center, n, hexagon_radius)

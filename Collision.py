from math import sqrt
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def plot_polygons(P, Q):
    P_x = [point[0] for point in P]
    P_y = [point[1] for point in P]
    Q_x = [point[0] for point in Q]
    Q_y = [point[1] for point in Q]

    plt.figure()
    plt.fill(P_x, P_y, "b")  # Plot P in blue
    plt.fill(Q_x, Q_y, "r")  # Plot Q in red
    plt.show()

def find_collision_point(P, Q):
    poly1 = Polygon(P)
    poly2 = Polygon(Q)
    intersection = poly1.intersection(poly2)
    if intersection.is_empty:
        print("No collision detected")
    elif intersection.geom_type == 'Point':
        print("Collision detected at:", intersection.coords[0])
    elif intersection.geom_type == 'LineString':
        print("Edge collision detected.")
        for point in intersection.coords:
            print("Collision detected at:", point)
    else:
        print("Complex collision detected.")
        # Handle more complex collision cases if needed

def separating_axis_theorem(vertices_a, vertices_b):
    edges = vertices_to_edges(vertices_a) + vertices_to_edges(vertices_b)
    axes = [normalize(orthogonal(edge_direction(*edge))) for edge in edges]

    for axis in axes:
        projection_a = project(vertices_a, axis)
        projection_b = project(vertices_b, axis)

        overlapping = (projection_a[0] <= projection_b[1]) and (projection_b[0] <= projection_a[1])

        if not overlapping:
            return False

    return True

def normalize(vector):
    """
    :return: The vector scaled to a length of 1
    """
    norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / norm, vector[1] / norm

def edge_direction(point0, point1):
    """
    :return: A vector going from point0 to point1
    """
    return point1[0] - point0[0], point1[1] - point0[1]

def vertices_to_edges(vertices):
    """
    :return: A list of the edges of the vertices as lists of points
    """
    return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]

def project(vertices, axis):
    """
    :return: A vector showing how much of the vertices lies along the axis
    """
    dots = [dot(vertex, axis) for vertex in vertices]
    return [min(dots), max(dots)]

def dot(vector1, vector2):
    """
    :return: The dot (or scalar) product of the two vectors
    """
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def orthogonal(vector):
    """
    :return: A new vector which is orthogonal to the given vector
    """
    return vector[1], -vector[0]

def main():
    # Define your polygons P and Q
    # P = [(0, 0), (0, 50), (50, 50), (50, 0)]
    # Q = [(100, 70), (180, 70), (100, 150)]

    # P = [(0, 10), (0, 60), (60, 60), (60, 10)]
    # Q = [(100, 40), (150, 40), (150, 90), (100, 90)]

    # P = [(0, 0), (30, 60), (60, 0)]  # Triangle P
    # Q = [(100, 80), (130, 20), (160, 80)]  # Triangle Q
    
    P = [(0, 0), (30, 20), (50, 60), (20, 80), (0, 50)]  # Random-shaped polygon P
    Q = [(90, 40), (140, 40), (140, 90), (90, 90)]  # Square Q





    # Define the translation step
    dx = 10

    # Translate P towards Q until they collide or reach a maximum number of steps
    max_steps = 18
    for step in range(max_steps):
        if separating_axis_theorem(P, Q):
            print("No collision detected")
            break
        
        # Translate P
        P = [(x+dx, y) for x, y in P]
        
        # Plot the polygons
        plot_polygons(P, Q)

        # Print the current state of P for debugging
        print("Current state of P:", P)
    else:
        print("Collision not detected within the maximum number of steps")

    # Now P and Q are colliding. Find and return the first point of collision.
    find_collision_point(P, Q)

if __name__ == "__main__":
    main()

from Polygon import myPolygon
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MatplotlibPolygon
import pickle


def squared_map(number):
    ids = [1]
    polygons = []
    centers = [(0, 0)]
    while len(centers) < number:
        for x, y in centers:
            if (x + 1, y) not in centers and len(centers) < number:
                centers.append((x + 1, y))
                ids.append(ids[-1] + 1)
            if (x + 1, y + 1) not in centers and len(centers) < number:
                centers.append((x + 1, y + 1))
                ids.append(ids[-1] + 1)
            if (x, y + 1) not in centers and len(centers) < number:
                centers.append((x, y + 1))
                ids.append(ids[-1] + 1)

    i = 0
    for x, y in centers:
        polygon = myPolygon()
        polygon.add_point((x, y))
        polygon.add_point((x + 1, y))
        polygon.add_point((x + 1, y + 1))
        polygon.add_point((x, y + 1))
        polygons.append(polygon)
        # polygon.get_points()
        polygon.set_id(ids[i])
        i += 1

    # List of objects of the class Polygon
    return polygons


def hexagoned_map(number):
    """Fpr each center of a hexagon, calculates the centers of all the hexagons with border intersection, until the input of hexagons is reached. Finally calculates the vertices of every hexagon.

    Args:
        number (_type_): _description_

    Returns:
        _type_: _description_
    """
    ids = [1]
    polygons = []

    centers = [(1, 3 / 4)]
    while len(centers) < number:
        for x, y in centers:
            if (x + 3 / 2, y + 3 / 4) not in centers and len(centers) < number:
                centers.append((x + 3 / 2, y + 3 / 4))
                ids.append(ids[-1] + 1)
            if (x, y + 3 / 2) not in centers and len(centers) < number:
                centers.append((x, y + 3 / 2))
                ids.append(ids[-1] + 1)
            if (x - 3 / 2, y + 3 / 4) not in centers and len(centers) < number:
                centers.append((x - 3 / 2, y + 3 / 4))
                ids.append(ids[-1] + 1)
            if (x - 3 / 2, y - 3 / 4) not in centers and len(centers) < number:
                centers.append((x - 3 / 2, y - 3 / 4))
                ids.append(ids[-1] + 1)
            if (x, y - 3 / 2) not in centers and len(centers) < number:
                centers.append((x, y - 3 / 2))
                ids.append(ids[-1] + 1)
            if (x + 3 / 2, y - 3 / 4) not in centers and len(centers) < number:
                centers.append((x + 3 / 2, y - 3 / 4))
                ids.append(ids[-1] + 1)

    i = 0
    for x, y in centers:
        polygon = myPolygon()
        polygon.add_point((x + 1, y))
        polygon.add_point((x + 1 / 2, y + 3 / 4))
        polygon.add_point((x - 1 / 2, y + 3 / 4))
        polygon.add_point((x - 1, y))
        polygon.add_point((x - 1 / 2, y - 3 / 4))
        polygon.add_point((x + 1 / 2, y - 3 / 4))
        polygons.append(polygon)
        polygon.set_id(ids[i])
        i += 1
        # polygon.get_points()

    # List of objects of the class Polygon
    return polygons


def draw_map(polygons, filename="polygon_map.png"):
    fig, ax = plt.subplots()

    for polygon in polygons:
        poly = MatplotlibPolygon(
            polygon.get_points(), edgecolor="black", facecolor="white"
        )
        ax.add_patch(poly)

        center_x, center_y = polygon.get_center()
        id = polygon.get_id()
        ax.text(center_x, center_y, str(id), ha="center", va="center", fontsize=12)

    # Automatically adjust the axis limits
    ax.autoscale()

    # Set equal aspect ratio to make squares appear as squares
    ax.set_aspect("equal")

    # Remove the axis
    ax.axis("off")

    # Save the image as a PNG file
    plt.savefig(filename, dpi=300, bbox_inches="tight")

    # Show the plygon
    # plt.show()


def get_polygon_by_id(polygons, id):
    for polygon in polygons:
        if polygon.get_id() == id:
            return polygon


def export_map(polygons, name):
    with open(name, "wb") as file:
        pickle.dump(polygons, file)
    print(f"Objects saved with success.")


def ImportPolygons(name):
    with open(name, "rb") as file:
        polygons = pickle.load(file)
    print(f"Objects loaded with success.")
    return polygons

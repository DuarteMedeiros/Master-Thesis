import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MatplotlibPolygon
import os


class myPolygon:
    def __init__(self):
        self.points = []
        self.name = ""

    def set_id(self, id):
        # Sets an id to a polygon
        self.id = id

    def set_name(self, name):
        # Sets an id to a polygon
        self.name = name

    def get_id(self):
        # returns the id of a polygon
        return self.id

    def get_name(self):
        # Sets an id to a polygon
        return self.name

    def add_point(self, point):
        # Adds a vertice to a polygon
        self.points.append(point)
        self.sort_points_clockwise()

    def real_add_point(self, point):
        # Adds a vertice to a polygon
        if point not in self.points:
            self.points.append(point)

    def get_points(self):
        # returns the points of a polygon
        return self.points

    def sort_points_clockwise(self):
        # Calculate the centroid of the polygon
        cx = sum(x for x, _ in self.points) / len(self.points)
        cy = sum(y for _, y in self.points) / len(self.points)

        # Sort the points based on their angle with respect to the centroid
        self.points.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

    def get_center(self):
        # calculates the center of the polygon
        x = 0
        y = 0
        n = len(self.points)
        for i, j in self.points:
            x += i
            y += j
        return x / n, y / n

    def get_max_distance(self):
        # calculates the maximum distance between any two vertices of a polygon
        max_distance = 0
        # first vertex
        for x1, y1 in self.points:
            # second vertex
            for x2, y2 in self.points:
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)
                if distance > max_distance:
                    max_distance = distance
        return max_distance

    def find_neighbors(self, other_polygons):
        # Returns the polygon objects and the polygons neighbours of a polygon, given a map of polygons
        # For a polygon to be a neighbour with another they have to share at least an edge
        neighbors = []
        neighbors_id = []
        for i, other_polygon in enumerate(other_polygons):
            # Skip comparing with itself
            if other_polygon is self:
                continue

            # Check if this polygon shares an edge with the other polygon
            if self.shares_edge_with(other_polygon):
                neighbors.append(other_polygon)
                neighbors_id.append(other_polygon.get_id())

        return neighbors, neighbors_id

    def shares_edge_with(self, other_polygon):
        for i in range(len(self.points)):
            point1 = self.points[i]
            point2 = self.points[
                (i + 1) % len(self.points)
            ]  # Wrap around for the last edge

            for j in range(len(other_polygon.points)):
                other_point1 = other_polygon.points[j]
                other_point2 = other_polygon.points[(j + 1) % len(other_polygon.points)]

                # Check if the edges have the same points (in any order)
                if (point1 == other_point1 and point2 == other_point2) or (
                    point1 == other_point2 and point2 == other_point1
                ):
                    return True

        return False

    def get_edges(self):
        # Generate edges from the sorted vertices
        edges = []
        for i in range(len(self.points)):
            edge = [self.points[i], self.points[(i + 1) % len(self.points)]]
            edges.append(edge)
        return edges

    def get_common_perimeter(self, other_polygon):
        # Calculate the common perimeter between two polygons
        edges1 = self.get_edges()
        edges2 = other_polygon.get_edges()

        common_perimeter = 0

        for e1 in edges1:
            for e2 in edges2:
                # print(f"edge = {e1} edge -1 = {e1[::-1]}")
                if e1 == e2 or e1[::-1] == e2:
                    x1, y1 = e1[0]
                    x2, y2 = e1[1]
                    deltax = x1 - x2
                    deltay = y1 - y2
                    common_perimeter += ((deltax) ** 2 + (deltay) ** 2) ** 0.5

        return common_perimeter

    def get_perimeter(self):
        # calculates the perimeter of a polygon
        lengths = []
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            lengths.append(distance)
        x1, y1 = self.points[0]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        lengths.append(distance)
        return sum(lengths)

    def get_area(self):
        # calculates the area of a polygon usong the sholace formula
        area = 0
        for i in range(len(self.points)):
            if i == len(self.points) - 1:
                x1, y1 = self.points[i]
                x2, y2 = self.points[0]
            else:
                x1, y1 = self.points[i]
                x2, y2 = self.points[i + 1]
            area += x1 * y2 - x2 * y1

        area = abs(area) / 2.0
        return area

    def draw_polygon(self):
        # draws the polygon
        fig, ax = plt.subplots()
        poly = MatplotlibPolygon(self.points, edgecolor="black", facecolor="white")
        ax.add_patch(poly)
        center_x, center_y = self.get_center()
        ax.text(center_x, center_y, str(self.id), ha="center", va="center", fontsize=12)
        ax.autoscale()

        # Set equal aspect ratio to make squares appear as squares
        ax.set_aspect("equal")
        # Remove the axis
        ax.axis("off")
        # Save the image as a PNG file
        plt.savefig(f"random_polygon_{self.id}.png", dpi=300, bbox_inches="tight")
        # Show the plygon
        plt.show()

    def save_polygon(self, Dataset=None):
        if Dataset == None:
            path = r"Real_Polygon_Examples\\"
        else:
            if not os.path.exists(r"Real_Polygon_Examples\\" + Dataset):
                os.mkdir(r"Real_Polygon_Examples\\" + Dataset)
            path = r"Real_Polygon_Examples\\" + Dataset + "\\"
        # saves the polygon in a file
        fig, ax = plt.subplots()
        poly = MatplotlibPolygon(self.points, edgecolor="black", facecolor="white")
        ax.add_patch(poly)
        center_x, center_y = self.get_center()
        ax.text(center_x, center_y, str(self.id), ha="center", va="center", fontsize=12)
        ax.autoscale()

        # Set equal aspect ratio to make squares appear as squares
        ax.set_aspect("equal")
        # Remove the axis
        ax.axis("off")
        # Save the image as a PNG file
        plt.savefig(
            f"{path}{self.name}_{self.id}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close("all")

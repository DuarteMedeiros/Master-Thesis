import pandas as pd
from Polygon import myPolygon
import pickle
import json
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MatplotlibPolygon
import matplotlib.colors as mcolors
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import random
import os
import sys
import statistics
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
import shapely.plotting
from shapely.geometry import Polygon

def import_polygons(name):
    """Given a pickle file import the polygons at the file

    Args:
        name (str): path of the pickle file

    Returns:
        list: list of polygons created with the class myPolygon
    """
    # read the pickle file
    with open(name, "rb") as file:
        polygons = pickle.load(file)
    print(f"Objects loaded with success.\n\n")
    return polygons


def draw_map(polygons, filename="polygon_map.png", write_id=True):
    fig, ax = plt.subplots()

    for polygon in polygons:
        #poly = Polygon(polygon.get_points())
        poly = MatplotlibPolygon(polygon.get_points(),edgecolor="black",facecolor="white")

        ax.add_patch(poly)
        #shapely.plotting.plot_polygon(ax, poly, facecolor='white', edgecolor='black')

        if write_id:
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
    #plt.savefig(filename, dpi=300, bbox_inches="tight")

    # Show the plygon
    plt.show()
    
polygons = import_polygons(r"Auxiliary_Files\Dataset_2 - 96 Conc_Map.pkl")
draw_map(polygons, write_id=False)
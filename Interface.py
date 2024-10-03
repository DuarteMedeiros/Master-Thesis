import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, simpledialog, messagebox
from ReadPolygons import import_polygons
from ReadPolygons import export_polygons
from ReadPolygons import hexagoned_map
from ReadPolygons import squared_map
from ReadPolygons import get_polygon_by_id
from copy import deepcopy
from Polygon import myPolygon
from matplotlib.patches import Polygon as MatplotlibPolygon
import sys
import pickle


class MapEditor:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Discret Map Editor")

        # Initialize variables
        self.map_data = None

        # Create a button select a map
        self.select_map_btn = tk.Button(
            root, text="Select Map", command=self.select_map
        )
        self.select_map_btn.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        # Create a button to sava a map
        self.save_map_btn = tk.Button(root, text="Save Map", command=self.save_map)
        self.save_map_btn.grid(row=0, column=2, pady=5, padx=10, sticky="w")

        # Create a button to add a new map
        self.new_map_btn = tk.Button(root, text="New Map", command=self.new_map)
        self.new_map_btn.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        # Create a button to add a polygon
        self.add_polygon_btn = tk.Button(
            root, text="Add Polygon", command=self.add_polygon
        )
        self.add_polygon_btn.grid(row=0, column=3, pady=5, padx=10, sticky="w")

        # Create a button to remove a polygon
        self.remove_polygon_btn = tk.Button(
            root, text="Remove Polygon", command=self.remove_polygon
        )
        self.remove_polygon_btn.grid(row=0, column=4, pady=5, padx=10, sticky="w")

        # Create a button to delete all drawings
        self.delete_drawings_btn = tk.Button(
            root, text="Delete Map", command=self.delete_drawings
        )
        self.delete_drawings_btn.grid(row=0, column=5, pady=5, padx=10, sticky="w")

        # Initialize an empty list for polygons
        self.polygons = []
        self.type = ""

        # Create map canvas
        self.map_canvas = FigureCanvasTkAgg(plt.figure(), master=self.root)
        self.map_canvas.get_tk_widget().grid(
            row=1, column=0, columnspan=7, pady=5, padx=10, sticky="nsew"
        )

        # Configure row and column weights to make canvas expandable
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        root.protocol("WM_DELETE_WINDOW", self.save_data_on_close)

    def select_map(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            # Import the polygons from a .pkl file
            self.polygons = import_polygons(file_path)
            polygon = self.polygons[0]
            if len(polygon.get_points()) == 4:
                self.type = "Square"
            elif len(polygon.get_points()) == 6:
                self.type = "Hexagon"
            else:
                None
            print(self.type)
            self.draw_map()

    def draw_map(self):
        # Draw the map using matplotlib in the already open window
        plt.clf()
        fig, ax = plt.gcf(), plt.gca()
        for polygon in self.polygons:
            # Assuming myPolygon has a method to draw itself
            # Replace this with your logic to draw polygons
            poly = MatplotlibPolygon(
                polygon.get_points(),
                edgecolor="black",
                facecolor="white",
            )
            ax.add_patch(poly)

            center_x, center_y = polygon.get_center()
            id = polygon.get_id()
            ax.text(center_x, center_y, str(id), ha="center", va="center", fontsize=12)

        # plt.title("Map")
        plt.axis("equal")  # Ensure the aspect ratio is maintained
        plt.axis("off")
        plt.draw()

    def delete_drawings(self):
        # Delete all drawings by clearing the self.polygons list
        self.polygons = []
        self.draw_map()  # Redraw the map to reflect the changes

    def save_map(self):
        # Save the map using the save_map function (replace with your own saving logic)
        if self.polygons != []:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")]
            )
            if file_path:
                # Save map data to the selected pickle file
                export_polygons(self.polygons, file_path)

            self.delete_drawings(self)
        else:
            tk.messagebox.showerror("Error", "There is no map.")

    def new_map(self):
        exists_n = False
        # Ask the user for the type of map (Square or Hexagon)
        map_type = simpledialog.askstring(
            "Map Type", "Choose map type (Square or Hexagon):", parent=self.root
        )

        try:
            map_type, num_polygons = map_type.split(" ")
            num_polygons = int(num_polygons)
            exists_n = True

        except:
            exists_n = False

        if map_type and map_type.lower() in ["square", "hexagon", "h", "s"]:
            if not (exists_n):
                # Ask the user for the number of polygons
                num_polygons = simpledialog.askinteger(
                    "Number of Polygons",
                    "Enter the number of polygons:",
                    parent=self.root,
                )
            if num_polygons is not None:
                # Generate a new map based on the user's choices
                if map_type.lower() in ["square", "s"]:
                    self.polygons = squared_map(num_polygons)
                    self.type = "Square"
                elif map_type.lower() in ["hexagon", "h"]:
                    self.polygons = hexagoned_map(num_polygons)
                    self.type = "Hexagon"
                else:
                    tk.messagebox.showerror("Error", "Something went wrong.")
                    return

                # Draw the new map
                self.draw_map()
        else:
            tk.messagebox.showerror("Error", "Invalid map type.")

    def add_polygon(self):
        exists_id = False
        # Check if self.polygons is empty
        if not self.polygons:
            tk.messagebox.showinfo(
                "Map Modification", "Cannot modify the map. Please create a map first."
            )
            return
        if self.type == "Square":
            # Ask the user for the direction (Left, Right, Up, or Down)
            direction = simpledialog.askstring(
                "Add Polygon",
                "Choose direction (Left, Right, Up, or Down):",
                parent=self.root,
            )

            try:
                print(f"Valores = {direction}")
                direction, polygon_id = direction.split(" ")
                print(f"direction = {direction}")
                print(f"id = {polygon_id}")
                polygon_id = int(polygon_id)
                exists_id = True
            except:
                exists_id = False

            if direction and direction.lower() in [
                "left",
                "right",
                "up",
                "down",
                "u",
                "d",
                "r",
                "l",
            ]:
                # Ask the user for the ID of the polygon next to which the modification should occur
                if not (exists_id):
                    polygon_id = simpledialog.askinteger(
                        "Add Polygon", "Enter the ID of the polygon:", parent=self.root
                    )
                if polygon_id is not None and polygon_id <= len(self.polygons):
                    self.add_polygon_action(direction, polygon_id)
                else:
                    tk.messagebox.showerror(
                        "Error", f"There is no polygon with id {polygon_id}."
                    )
            else:
                tk.messagebox.showerror("Error", "Invalid direction.")
        elif self.type == "Hexagon":
            # Ask the user for the direction (Left, Right, Up, or Down)
            direction = simpledialog.askstring(
                "Add Polygon",
                "Choose direction (LeftUp, LeftDown, RightUp, RightDown, Up, or Down):",
                parent=self.root,
            )

            try:
                # print(f"Valores = {direction}")
                direction, polygon_id = direction.split(" ")
                # print(f"direction = {direction}")
                # print(f"id = {polygon_id}")
                polygon_id = int(polygon_id)
                exists_id = True
            except:
                exists_id = False

            if direction and direction.lower() in [
                "leftup",
                "leftdown",
                "rightup",
                "rightdown",
                "up",
                "down",
                "u",
                "d",
                "ru",
                "rd",
                "lu",
                "ld",
            ]:
                if not (exists_id):
                    # Ask the user for the ID of the polygon next to which the modification should occur
                    polygon_id = simpledialog.askinteger(
                        "Add Polygon", "Enter the ID of the polygon:", parent=self.root
                    )
                if polygon_id is not None and polygon_id <= len(self.polygons):
                    self.add_polygon_action(direction, polygon_id)
                else:
                    tk.messagebox.showerror(
                        "Error", f"There is no polygon with id {polygon_id}."
                    )
            else:
                tk.messagebox.showerror("Error", "Invalid direction.")

    def remove_polygon(self):
        # Check if self.polygons is empty
        if not self.polygons:
            tk.messagebox.showinfo(
                "Map Modification", "Cannot modify the map. Please create a map first."
            )
            return

        # Ask the user for the ID of the polygon next to which the modification should occur
        polygon_id = simpledialog.askinteger(
            "Remove Polygon", "Enter the ID of the polygon:", parent=self.root
        )
        if polygon_id is not None and polygon_id <= len(self.polygons):
            self.remove_polygon_action(polygon_id)
        else:
            tk.messagebox.showerror(
                "Error", f"There is no polygon with id {polygon_id}."
            )

    def add_polygon_action(self, direction, polygon_id):
        # Add a polygon based on the user's choices
        print(f"Adding polygon {direction} next to ID {polygon_id}.")

        list_centers = []
        for polygon in self.polygons:
            center = polygon.get_center()
            list_centers.append(center)

        polygons = deepcopy(self.polygons)
        polygon = get_polygon_by_id(self.polygons, polygon_id)

        if self.type == "Square":
            x, y = polygon.get_center()
            if direction.lower() == "right" or direction.lower() == "r":
                x = x + 1
                y = y
            elif direction.lower() == "left" or direction.lower() == "l":
                x = x - 1
                y = y
            elif direction.lower() == "up" or direction.lower() == "u":
                x = x
                y = y + 1
            elif direction.lower() == "down" or direction.lower() == "d":
                x = x
                y = y - 1
            if (x, y) not in list_centers:
                new_polygon = myPolygon()
                new_polygon.add_point((x - 0.5, y - 0.5))
                new_polygon.add_point((x + 0.5, y - 0.5))
                new_polygon.add_point((x + 0.5, y + 0.5))
                new_polygon.add_point((x - 0.5, y + 0.5))
            else:
                tk.messagebox.showerror(
                    "Error", "There is already a polygon in that place."
                )
                return None

        elif self.type == "Hexagon":
            x, y = polygon.get_center()
            if direction.lower() == "down" or direction.lower() == "d":
                x = x
                y = y - 3 / 2
            elif direction.lower() == "up" or direction.lower() == "u":
                x = x
                y = y + 3 / 2
            elif direction.lower() == "rightup" or direction.lower() == "ru":
                x = x + 3 / 2
                y = y + 3 / 4
            elif direction.lower() == "rightdown" or direction.lower() == "rd":
                x = x + 3 / 2
                y = y - 3 / 4
            elif direction.lower() == "leftup" or direction.lower() == "lu":
                x = x - 3 / 2
                y = y + 3 / 4
            elif direction.lower() == "leftdown" or direction.lower() == "ld":
                x = x - 3 / 2
                y = y - 3 / 4
            if (x, y) not in list_centers:
                new_polygon = myPolygon()
                new_polygon.add_point((x + 1, y))
                new_polygon.add_point((x + 1 / 2, y + 3 / 4))
                new_polygon.add_point((x - 1 / 2, y + 3 / 4))
                new_polygon.add_point((x - 1, y))
                new_polygon.add_point((x - 1 / 2, y - 3 / 4))
                new_polygon.add_point((x + 1 / 2, y - 3 / 4))
            else:
                tk.messagebox.showerror(
                    "Error", "There is already a polygon in that place."
                )
                return None

        polygons.append(new_polygon)
        new_polygon.set_id(len(polygons))
        self.delete_drawings()
        self.polygons = deepcopy(polygons)
        self.draw_map()

    def remove_polygon_action(self, polygon_id):
        polygon = get_polygon_by_id(self.polygons, polygon_id)
        self.polygons.remove(polygon)
        polygons = deepcopy(self.polygons)
        # print(polygons)
        self.delete_drawings()
        self.polygons = deepcopy(polygons)
        id = 1
        for polygon in self.polygons:
            polygon.set_id(id)
            id += 1
        self.draw_map()

    def save_data_on_close(self):
        # Save data when the app is closed
        if self.polygons:
            # Ask the user for the file path to save the data
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")]
            )
            if file_path:
                try:
                    with open(file_path, "wb") as file:
                        pickle.dump(self.polygons, file)
                    messagebox.showinfo("Save Successful", "Data saved successfully.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"An error occurred while saving: {e}"
                    )
        else:
            messagebox.showinfo("No Data to Save", "No data to save.")

        # Close the Tkinter window
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = MapEditor(root)
    root.geometry("800x600")  # Set an initial window size
    root.mainloop()

from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
from view.minimap import Minimap
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from pathlib import Path
import numpy as np
import math
import csv


class Core(ShowBase, DirectObject):
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    REFERENCE_ANGLE = 188
    PATHS = {
        "3D_SCENE_MODEL": "resource/cylinder.egg",
        "LOCATIONS_DB": "resource/location_file.txt",
        "MINIMAP_BG": "resource/minimap.png",
        "MINIMAP_POINT_MODEL": "resource/point.egg"
    }

    def __init__(self):
        super().__init__()

        self.locations = []
        self.active_view = None
        self.active_location = None
        self.scene_3d_model = None
        self.reference_point = None

        # load data
        self.load_data()
        self.set_reference_point()
        self.active_location = self.locations[0]

        # define views
        self.main_menu_view = MainMenuView(self)
        self.minimap = Minimap(self)
        self.scene_3d_view = Scene3DView(self)
        self.pause_menu_view = PauseMenuView(self)

        # set window size, load first view
        self.set_window_size()
        self.set_active_view(self.main_menu_view)

    def set_window_size(self):
        props = WindowProperties()
        props.setSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.win.requestProperties(props)

    def load_data(self):

        def process_coords():
            split_coords = row["map_coord"].split(',')
            map_x, map_y = [int(i) for i in split_coords]
            map_x_normed = ((map_x*2) / self.WINDOW_WIDTH) - 1
            map_y_normed = -(((map_y*2) / self.WINDOW_HEIGHT) - 1)
            return map_x_normed, map_y_normed

        def process_texture():
            texture_path = Path("resource/{}".format(row["texture"]))
            texture = self.loader.loadTexture(texture_path)
            return texture

        self.scene_3d_model = self.loader.loadModel(self.PATHS["3D_SCENE_MODEL"])
        with open(self.PATHS["LOCATIONS_DB"], "r") as l_file:
            data = csv.DictReader(l_file, delimiter="|")
            for row in data:
                id = row["id"]
                x, y = process_coords()
                neighbors = row["neighbors"].split(',')
                texture = process_texture()
                location = Location(id, x, y, neighbors, texture)
                location.reparentTo(self.render2d)
                self.locations.append(location)

    @staticmethod
    def calculate_displacement(origin, target, transpose=False):
        origin_x, origin_y = origin.get_position()
        target_x, target_y = target.get_position()
        if transpose:
            return np.array([[target_x - origin_x, target_y - origin_y]]).T
        else:
            return np.array([target_x - origin_x, target_y - origin_y])

    def set_reference_point(self):
        theta = 2*math.pi-math.radians(self.REFERENCE_ANGLE)
        origin = self.locations[0]
        target = self.locations[1]
        v = self.calculate_displacement(origin, target, transpose=True)
        v_norm = math.sqrt(v[0]**2+v[1]**2)
        rotation_matrix = np.matrix([[math.cos(theta), -math.sin(theta)],
                                     [math.sin(theta),  math.cos(theta)]])
        offset_x, offset_y = origin.get_position()
        self.reference_point = np.array([offset_x, offset_y])+np.transpose((1/v_norm)*rotation_matrix*v)
        pass

    def find_location_by_id(self, id):
        for location in self.locations:
            if location.id == id:
                return location
        return None

    def get_active_view(self):
        return self.active_view

    def get_active_location(self):
        return self.active_location

    def set_active_view(self, view):
        view.load_view()
        self.active_view = view

    def set_active_location(self, new_location):
        old_location = self.active_location
        for location in self.locations:
            if location is new_location:
                location.set_to_active()
                self.active_location = location
            else:
                location.set_to_inactive()
        texture = self.active_location.get_texture()
        self.scene_3d_model.setTexture(texture)
        print(old_location.get_position())
        print(new_location.get_position())
        print(self.reference_point)
        self.reference_point += self.calculate_displacement(old_location, new_location)
        print(self.reference_point)

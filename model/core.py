from model.location import Location
from model.logging import Logger
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
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print(method.__name__, args, kw, te - ts, "halál")
        return result

    return timed

class Core(ShowBase, DirectObject):
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT
    REFERENCE_ANGLE = 188
    PATHS = {
        "3D_SCENE_MODEL": "resource/models/cylinder.egg",
        "LOCATIONS_DB": "resource/locatin_file.txt",
        "MINIMAP_BG_TEXTURE": "resource/textures/minimap.png",
        "MINIMAP_BG_MODEL": "resource/models/minimap.egg",
        "MINIMAP_POINT_MODEL": "resource/models/point.egg",
        "LOCATION_MARKER_MODEL": "resource/models/arrow.egg",
        "LOCATION_MARKER_TEXTURE": "resource/textures/arrow.png"
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
        self.set_neighbor_markers()
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

    @Logger.runtime
    def load_data(self):

        @Logger.runtime
        def process_coords():
            split_coords = row["map_coord"].split(',')
            map_x, map_y = [int(i) for i in split_coords]
            map_x_normed = ((map_x*2) / 549) - 1
            map_y_normed = -(((map_y*2) / 549) - 1)
            return map_x_normed, map_y_normed

        @Logger.runtime
        def process_texture():
            texture_path = Path("resource/textures/{}".format(row["texture"]))
            texture = self.loader.loadTexture(texture_path)
            return texture

        self.scene_3d_model = self.loader.loadModel(self.PATHS["3D_SCENE_MODEL"])

        try:
            with open(self.PATHS["LOCATIONS_DB"], "r") as l_file:
                data = csv.DictReader(l_file, delimiter="|")
                for row in data:
                    id = int(row["id"])
                    x, y = process_coords()
                    neighbors = [int(neighbor_id) for neighbor_id in row["neighbors"].split(',')]
                    texture = process_texture()
                    location = Location(id, x, y, neighbors, texture)
                    location.reparentTo(self.render2d)
                    self.locations.append(location)
        except:
            Logger.log_file_not_found(self.PATHS["LOCATIONS_DB"])

    @staticmethod
    def calculate_displacement(origin_pos, target_pos, transpose=False):
        origin_x, origin_y = origin_pos
        target_x, target_y = target_pos
        if transpose:
            return np.array([[target_x - origin_x, target_y - origin_y]]).T
        else:
            return np.array([target_x - origin_x, target_y - origin_y])

    @Logger.runtime
    def set_reference_point(self):
        theta = 2*math.pi-math.radians(self.REFERENCE_ANGLE)
        origin_pos = self.locations[0].get_position()
        target_pos = self.locations[1].get_position()
        v = self.calculate_displacement(origin_pos, target_pos, transpose=True)
        v_norm = math.sqrt(v[0]**2+v[1]**2)
        rotation_matrix = np.matrix([[math.cos(theta), -math.sin(theta)],
                                     [math.sin(theta),  math.cos(theta)]])
        offset_x, offset_y = origin_pos
        reference_point_matrix = np.array([offset_x, offset_y])+np.transpose((1/v_norm)*rotation_matrix*v)
        self.reference_point = reference_point_matrix.tolist()[0]

    @Logger.runtime
    def set_neighbor_markers(self):
        marker_texture_path = self.PATHS["MINIMAP_BG_TEXTURE"]
        marker_texture = self.loader.loadTexture(marker_texture_path)
        for location in self.locations:
            location_pos = location.get_position()
            for neighbor_id in location.get_neighbors():
                neighbor = self.find_location_by_id(neighbor_id)
                neighbor_pos = neighbor.get_position()
                neighbor_displaced = self.calculate_displacement(location_pos, neighbor_pos)
                neighbor_displaced_x, neighbor_displaced_y = neighbor_displaced.tolist()

                reference_displaced = self.calculate_displacement(location_pos, self.reference_point)
                reference_displaced_x, reference_displaced_y = reference_displaced.tolist()

                dot_product = neighbor_displaced_x * reference_displaced_x + neighbor_displaced_y * reference_displaced_y
                displacement_norm = math.sqrt(neighbor_displaced_x ** 2 + neighbor_displaced_y ** 2)
                reference_norm = math.sqrt(reference_displaced_x ** 2 + reference_displaced_y ** 2)
                angle = math.degrees(math.acos(dot_product / (displacement_norm * reference_norm)))

                def reference_line(x_pos):
                    slope = reference_displaced_y / reference_displaced_x
                    return slope * x_pos

                if reference_line(neighbor_displaced_x) > neighbor_displaced_y:
                    angle = 360-angle

                location.add_neighbor_marker(neighbor, angle, marker_texture)

    @Logger.runtime
    def find_location_by_id(self, id):
        for location in self.locations:
            if location.id == id:
                return location
        return None

    @Logger.runtime
    def find_location_by_marker(self, marker):
        for location in self.locations:
            for neighbor_id in location.get_markers():
                neighbor = self.find_location_by_id(neighbor_id)
                _, loc_marker = location.get_markers()[neighbor_id]
                if marker == loc_marker:
                    return neighbor
                print(location.id)
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
        old_location_pos = old_location.get_position()
        new_location_pos = new_location.get_position()
        for location in self.locations:
            if location is new_location:
                location.set_to_active()
                self.active_location = location
            else:
                location.set_to_inactive()
        texture = self.active_location.get_texture()
        self.scene_3d_model.setTexture(texture)
        self.reference_point += self.calculate_displacement(old_location_pos, new_location_pos)

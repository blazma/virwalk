from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
from view.minimap import Minimap
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from pathlib import Path
import csv


class Core(ShowBase, DirectObject):
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
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

        # load data
        self.load_data()
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
        for location in self.locations:
            if location is new_location:
                location.set_to_active()
                self.active_location = new_location
            else:
                location.set_to_inactive()
        texture = self.active_location.get_texture()
        self.scene_3d_model.setTexture(texture)

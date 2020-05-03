from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from pathlib import Path
import csv


class Core(ShowBase, DirectObject):
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.locations = []
        self.active_view = None
        self.active_location = None

        # load data
        locations_file_path = Path("resource/location_file.txt")
        self.load_locations(locations_file_path)
        self.active_location = self.locations[0]

        # define views
        self.main_menu_view = MainMenuView(self)
        self.scene_3d_view = Scene3DView(self)
        self.pause_menu_view = PauseMenuView(self)

        # set window size, load first view
        self.set_window_size()
        self.set_active_view(self.main_menu_view)

    def set_window_size(self):
        props = WindowProperties()
        props.setSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.win.requestProperties(props)

    def load_locations(self, locations_file):

        def process_coords(row):
            split_coords = row["map_coord"].split(',')
            map_x, map_y = [int(i) for i in split_coords]
            map_x_normed = ((map_x*2) / self.WINDOW_WIDTH) - 1
            map_y_normed = -(((map_y*2) / self.WINDOW_HEIGHT) - 1)
            return map_x_normed, map_y_normed

        with open(locations_file, "r") as l_file:
            data = csv.DictReader(l_file, delimiter="|")
            for row in data:
                id = row["id"]
                x, y = process_coords(row)
                neighbors = row["neighbors"].split(',')
                texture = row["texture"]
                location = Location(id, x, y, neighbors, texture)
                self.locations.append(location)
                location.reparentTo(self.render2d)

    def find_location_by_id(self, id):
        for location in self.locations:
            if location.id == id:
                return location
        return None

    def get_active_view(self):
        return self.active_view

    def get_active_texture(self):
        return self.active_location.get_texture()

    def set_active_view(self, view):
        view.load_view()
        self.active_view = view

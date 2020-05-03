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
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    def __init__(self):
        super().__init__()

        self.locations = []
        self.active_view = None
        self.active_location = None

        # load data
        locations_file_path = Path("resource/location_file.txt")
        self.load_locations(locations_file_path)
        self.origin = self.locations[0]

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
        with open(locations_file, "r") as l_file:
            data = csv.DictReader(l_file, delimiter="|")
            for row in data:
                split_coord = [int(i) for i in row["map_coord"].split(',')]
                normed_coords = [((split_coord[0]*2) / 800) - 1, (((split_coord[1]*2) / 600) - 1) * (-1)]
                split_neighbors = row["neighbors"].split(',')
                current_location = Location(id=row["id"], neighbors=split_neighbors, texture=row["texture"], map_coord=normed_coords)
                self.locations.append(current_location)

    def get_active_view(self):
        return self.active_view

    def set_active_view(self, view):
        view.load_view()
        self.active_view = view

from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
import csv


class Core(ShowBase):
    def __init__(self):
        super().__init__()

        self.views = [MainMenuView, Scene3DView, PauseMenuView]
        self.locations = []
        self.active_view = None
        self.active_location = None

        self.load_locations("resource/location_file.txt")

    def load_locations(self, locations_file):
        with open(locations_file, "r") as l_file:
            data = csv.DictReader(l_file, delimiter="|")
            for row in data:
                split_coord = [int(i) for i in row["map_coord"].split(',')]
                split_neighbors = row["neighbors"].split(',')
                current_location = Location(id=row["id"], neighbors=split_neighbors, texture=row["texture"])
                self.locations.append(current_location)

    def get_view(self):
        return self.active_view

    def set_view(self, view):
        self.active_view = view

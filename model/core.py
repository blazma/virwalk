from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView


class Core:
    def __init__(self):
        self.views = [MainMenuView, Scene3DView, PauseMenuView]
        self.locations = []
        self.active_view = None
        self.active_location = None

        self.load_locations("resource/location_file.txt")

    def set_view(self, view):
        self.active_view = view

    def load_locations(self, locations_file):
        with open(locations_file, "r") as l_file:
            data = csv.DictReader(l_file, delimiter="|")
            for row in data:
                split_c = [int(i) for i in row["map_coord"].split(',')]
                split_n = row["neighbors"].split(',')
                print(row["id"], row["texture"], split_c, split_n)
                current_location = Location(id=row["id"], neighbors=split_n, texture=row["texture"])
                self.locations.append(current_location)

    def run_program(self):
        # Panda3D stuff probably
        # runs only once when the entire app is started
        self.set_view(MainMenuView)

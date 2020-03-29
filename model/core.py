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
            # process lines
            dummy_location = Location(id=0, neighbors=[3, 6, 7], texture="resource/photo00.jpg")
            self.locations.append(dummy_location)
            pass

    def run_program(self):
        # Panda3D stuff probably
        # runs only once when the entire app is started
        self.set_view(MainMenuView)

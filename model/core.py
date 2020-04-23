from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject


class Core(ShowBase, DirectObject):
    def __init__(self):
        super().__init__()

        #self.views = [MainMenuView, Scene3DView, PauseMenuView]
        self.locations = []
        self.active_location = None
        self.load_locations("resource/location_file.txt")

        # define views
        self.active_view = None
        self.scene_3d_view = Scene3DView(self)
        self.main_menu_view = MainMenuView(self)
        self.pause_menu_view = PauseMenuView(self)

        # Set the starter view to Main menu
        self.set_active_view(self.main_menu_view)

    def load_locations(self, locations_file):
        with open(locations_file, "r") as l_file:
            # process lines
            dummy_location = Location(id=0, neighbors=[3, 6, 7], texture="resource/photo00.jpg")
            self.locations.append(dummy_location)

    def get_active_view(self):
        return self.active_view

    def set_active_view(self, view):
        self.active_view = view
        self.show_active_view()

    def show_active_view(self):
        self.active_view.screen.show()

    def comm(self):
        print("Itt vagyok")
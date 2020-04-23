from model.location import Location
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties


class Core(ShowBase):
    WINDOW_WIDTH = 512
    WINDOW_HEIGHT = 1024

    def __init__(self):
        super().__init__()
        # declare variables
        self.scene = None
        self.locations = []
        self.active_view = None
        self.active_location = None

        # load data
        self.load_locations("resource/location_file.txt")
        self.origin = self.locations[0]

        # define views
        self.main_menu_view = MainMenuView(self)
        self.scene_3d_view = Scene3DView(self)
        self.pause_menu_view = PauseMenuView(self)

        # set window size, load first view
        self.set_window_size()
        print(self.camLens.getVfov())
        self.load_scene(self.scene_3d_view)

    def set_window_size(self):
        props = WindowProperties()
        props.setSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.win.requestProperties(props)

    def load_locations(self, locations_file):
        with open("resource\location_file.txt", "r") as l_file:
            # process lines
            dummy_location = Location(id=0, neighbors=[3, 6, 7], texture="resource/photo00.jpg")
            self.locations.append(dummy_location)
            pass

    def load_scene(self, view):
        self.scene = view.load_view()
        texture = self.loader.loadTexture("resource\photo01.jpg")
        self.scene.setTexture(texture)
        self.scene.reparentTo(self.render)
        self.scene.setScale(2.0, 2.0, 2.0)
        self.scene.setPos(self.camera.getPos())

    def get_view(self):
        return self.active_view

    def set_view(self, view):
        self.active_view = view

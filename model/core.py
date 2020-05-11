from model.location import Location
from model.logger import Logger
from view.main_menu_view import MainMenuView
from view.scene_3d_view import Scene3DView
from view.pause_menu_view import PauseMenuView
from view.minimap import Minimap
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor import Actor
from panda3d.core import WindowProperties
from pathlib import Path
import numpy as np
import math
import csv


class Core(ShowBase, DirectObject):
    """
    The heart of the program. We followed the Model-View paradigm; in our project we dedicated much effort to separate
    the data and calculations side of the program from the visualization and control side. This class represents the
    model, containing most of the back-end of the software: reading files, loading models and textures, setting views
    up, etc.
    """
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT
    REFERENCE_ANGLE = 188
    MINIMAP_DIM = 549
    PATHS = {
        "3D_SCENE_MODEL": "resource/models/cylinder.egg",
        "LOCATIONS_DB": "resource/location_file.txt",
        "MINIMAP_BG_TEXTURE": "resource/gui/minimap.png",
        "MINIMAP_BG_MODEL": "resource/models/minimap.egg",
        "MINIMAP_POINT_MODEL": "resource/models/point.egg",
        "LOCATION_MARKER_MODEL": "resource/models/arrow.egg",
        "LOCATION_MARKER_TEXTURE": "resource/gui/arrow.png",
        "INDICATOR_MODEL": "resource/models/indicator.egg",
        "MAIN_MENU_BG": "resource/gui/main_menu_background.png",
        "MAIN_MENU_START": "resource/gui/main_menu_start.png",
        "MAIN_MENU_QUIT": "resource/gui/quit.png",
        "PAUSE_MENU_BACK": "resource/gui/pause_menu_back_to_mm.png",
        "PAUSE_MENU_CONTINUE": "resource/gui/pause_menu_continue.png",
        "OPTIONS_BUTTON": "resource/gui/options.png"
    }

    def __init__(self):
        super().__init__()

        # declaration of the most important variables
        self.locations = []
        self.active_view = None
        self.active_location = None
        self.scene_3d_model = None
        self.reference_point = None
        self.indicator = None

        # load data
        self.load_data()
        self.set_reference_point()
        self.set_neighbor_markers()
        self.create_direction_indicator()

        # define views
        self.main_menu_view = MainMenuView(self)
        self.minimap = Minimap(self)
        self.scene_3d_view = Scene3DView(self)
        self.pause_menu_view = PauseMenuView(self)

        # set window size, load first view
        self.set_window_size()
        self.set_active_view(self.main_menu_view)

        # fine-tuning parameters
        self.rot_sens_unit = 1.0
        self.zoom_sens_unit = 0.01
        self.rotation_sensitivity = 1.0
        self.zoom_sensitivity = 0.01

    def set_window_size(self):
        props = WindowProperties()
        props.setSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.win.requestProperties(props)

    @Logger.runtime
    def load_data(self):
        """
        This method reads the location database file and processes the data such that Location objects are created
        and stored.
        """
        @Logger.runtime
        def process_coords():
            """
            The placement of locations on our minimap is crucial. Panda3D objects however have a coordinate range from
            -1 to 1 on all axis, meaning that if we read a coordinate of a location from some image processing software
            by hand, we have to transform those coordinates into coordinates Panda would understand. This function does
            just that.
            :return: Normalized coordinates of location coordinates.
            """
            split_coords = row["map_coord"].split(',')
            map_x, map_y = [int(i) for i in split_coords]
            map_x_normed = ((map_x*2) / self.MINIMAP_DIM) - 1
            map_y_normed = -(((map_y*2) / self.MINIMAP_DIM) - 1)
            return map_x_normed, map_y_normed

        @Logger.runtime
        def process_texture():
            texture_path = Path("resource/textures/{}".format(row["texture"]))
            texture = self.loader.loadTexture(texture_path)
            return texture

        # the cylinder is loaded here but it does not yet show up, until it's specifically asked to
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
                Logger.log_info('The locations_db has been loaded')
        except:
            Logger.error('{} file not found!'.format(self.PATHS["LOCATIONS_DB"]))

        self.active_location = self.locations[0]

    @staticmethod
    def calculate_displacement(origin_pos, target_pos, transpose=False):
        """
        Helper function, calculates the difference vector betweeen two vectors in 2 dimensions.
        :param origin_pos: the coordinates of the starting point
        :param target_pos: the coordinates of the endpoint
        :param transpose: if True returns with transpose of results, if False it does not
        :return: 2D array containing vector coordinates of difference vector
        """
        origin_x, origin_y = origin_pos
        target_x, target_y = target_pos
        if transpose:
            return np.array([[target_x - origin_x, target_y - origin_y]]).T
        else:
            return np.array([target_x - origin_x, target_y - origin_y])

    @Logger.runtime
    def set_reference_point(self):
        """
        The reference point is one of the most important concepts. It's an arbitrary point in space with respect to
        which every angle is calculated. These angles are important as they are the ones that determine where a user-
        clickable direction marker will be placed.
        """
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

    def calculate_angle(self, v, w):
        v_x, v_y = v
        w_x, w_y = w
        dot_product = v_x * w_x + v_y * w_y
        v_norm = math.sqrt(v_x ** 2 + v_y ** 2)
        w_norm = math.sqrt(w_x ** 2 + w_y ** 2)
        return math.degrees(math.acos(dot_product / (v_norm * w_norm)))

    @Logger.runtime
    def set_neighbor_markers(self):
        """
        Goes through the neighbors of all the locations and creates the required markers that allow users to click
        on them and thus change between locations.
        :return:
        """
        marker_texture_path = self.PATHS["MINIMAP_BG_TEXTURE"]
        marker_texture = self.loader.loadTexture(marker_texture_path)
        for location in self.locations:
            location_pos = location.get_position()
            for neighbor_id in location.get_neighbors():
                neighbor = next(self.find_location_by_id(neighbor_id))
                neighbor_pos = neighbor.get_position()
                neighbor_displaced = self.calculate_displacement(location_pos, neighbor_pos).tolist()
                neighbor_displaced_x, neighbor_displaced_y = neighbor_displaced
                reference_displaced = self.calculate_displacement(location_pos, self.reference_point).tolist()
                reference_displaced_x, reference_displaced_y = reference_displaced
                angle = self.calculate_angle(neighbor_displaced, reference_displaced)

                def reference_line(x_pos):
                    slope = reference_displaced_y / reference_displaced_x
                    return slope * x_pos

                if reference_line(neighbor_displaced_x) > neighbor_displaced_y:
                    angle = 360-angle

                location.add_neighbor_marker(neighbor, angle, marker_texture)

    def create_direction_indicator(self):
        """
        The direction indicator is a tiny arrow on the minimap always pointing into the same direction as the camera.
        :return:
        """
        self.indicator = Actor.Actor(self.PATHS["INDICATOR_MODEL"])
        self.indicator.setColor(0, 0, 0, 1)
        self.indicator.setScale(Location.SCALE)
        loc_x, loc_y = self.active_location.get_position()
        self.indicator.setPos(loc_x, 0, loc_y)

        # the indicator faces north by default but we want it to face the reference angle
        indicator_vector = self.calculate_displacement(origin_pos=(loc_x, loc_y), target_pos=(loc_x, 1)).tolist()
        reference_displaced = self.calculate_displacement(origin_pos=(loc_x, loc_y), target_pos=self.reference_point).tolist()
        angle = self.calculate_angle(indicator_vector, reference_displaced)
        self.indicator.setR(angle)

    @Logger.runtime
    def find_location_by_id(self, id):
        """
        This generator finds a location based on the ID given.
        :param id: ID of the location we're looking for
        :return: location
        """
        for location in self.locations:
            if location.id == id:
                yield location

    @Logger.runtime
    def find_location_by_marker(self, marker):
        """
        This generator finds the location by a given marker
        :param marker: marker model
        :return: location
        """
        for location in self.locations:
            for neighbor_id in location.get_markers():
                neighbor = next(self.find_location_by_id(neighbor_id))
                _, loc_marker = location.get_markers()[neighbor_id]
                if marker == loc_marker:
                    yield neighbor

    def get_active_view(self):
        return self.active_view

    def get_active_location(self):
        return self.active_location

    def set_active_view(self, view):
        view.load_view()
        self.active_view = view
        Logger.log_info('Active view has been set to {}'.format(view))

    def set_rotation_sensitivity(self):
        self.rotation_sensitivity = self.rot_sens_unit * self.scene_3d_view.get_rotation_sensitivity()

    def set_zoom_sensitivity(self):
        self.zoom_sensitivity = self.zoom_sens_unit * self.scene_3d_view.get_zoom_sensitivity()

    def set_active_location(self, new_location):
        """
        This function gets called whenever the user changes from one location to then next. The old locations markers
        must be hidden, the new location's markers must appear instea, etc.
        :param new_location: the target location of the user
        """
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
        Logger.log_info('Active location has been set from {} to {}'.format(old_location.id, new_location.id))

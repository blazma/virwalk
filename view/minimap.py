from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import LineSegs


class Minimap:
    MINIMAP_POSITION = (0.7, 0.0, -0.7)
    MINIMAP_SCALE = 0.25
    LINE_THICKNESS = 2.25

    def __init__(self, core):
        self.core = core
        self.locations = self.core.locations
        self.screen = DirectFrame(frameColor=(0, 0, 0, 1), parent=self.core.render2d)
        self.map = None

        self.draw_background()
        self.draw_lines()
        self.draw_points()
        self.screen.hide()

    def draw_background(self):
        background_path = self.core.PATHS["MINIMAP_BG"]
        position = self.MINIMAP_POSITION
        scale = self.MINIMAP_SCALE
        self.map = OnscreenImage(image=background_path, pos=position, scale=scale, parent=self.screen)

    def draw_points(self):
        for location in self.locations:
            location.reparentTo(self.map)

    def draw_lines(self):
        linesegs = LineSegs()
        linesegs.setColor(0.0, 0.0, 0.0, 0.0)
        linesegs.setThickness(2.25)
        for location in self.locations:
            loc_x, loc_y = location.get_position()
            linesegs.moveTo(loc_x, 0.0, loc_y)
            for neighbor_id in location.get_neighbors():
                neighbor = self.core.find_location_by_id(neighbor_id)
                nb_x, nb_y = neighbor.get_position()
                linesegs.drawTo(nb_x, 0.0, nb_y)
                linesegs.moveTo(loc_x, 0.0, loc_y)
        line_node = linesegs.create()
        self.map.attachNewNode(line_node)

    def show(self):
        self.screen.show()

    def hide(self):
        self.screen.hide()

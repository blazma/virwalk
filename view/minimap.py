from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import LineSegs


class Minimap:
    def __init__(self, core):
        self.core = core
        self.locations = self.core.locations
        self.screen = DirectFrame(frameColor=(0, 0, 0, 1), parent=self.core.render2d)
        self.map = OnscreenImage(image="resource/minimap.png", pos=(0.7, 0.0, -0.7), scale=0.25, parent=self.screen)
        self.draw_points()
        self.draw_lines()
        self.screen.hide()

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

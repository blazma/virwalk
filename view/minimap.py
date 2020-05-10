from direct.gui.DirectFrame import DirectFrame
from panda3d.core import LineSegs
from panda3d.core import TransparencyAttrib
from direct.actor.Actor import Actor
from panda3d.core import CardMaker


class Minimap:
    MINIMAP_POSITION = (0.7, 0.0, -0.7)
    MINIMAP_SCALE = 0.25
    LINE_THICKNESS = 2.25

    def __init__(self, core):
        self.core = core
        self.locations = self.core.locations
        scaling_vector = (self.MINIMAP_SCALE/self.core.ASPECT_RATIO, 0, self.MINIMAP_SCALE)
        self.screen = DirectFrame(frameColor=(0, 0, 0, 1), pos=self.MINIMAP_POSITION,
                                  scale=scaling_vector, parent=self.core.render2d)
        self.map = None
        self.indicator = self.core.indicator
        self.draw_background()
        self.draw_lines()
        self.draw_points()
        self.draw_indicator()
        self.screen.hide()

    def draw_background(self):
        background_model_path = self.core.PATHS["MINIMAP_BG_MODEL"]
        background_texture_path = self.core.PATHS["MINIMAP_BG_TEXTURE"]
        self.map = Actor(background_model_path)
        self.map.setTransparency(TransparencyAttrib.MAlpha)
        self.map.setColor(1,1,1,1)
        texture = self.core.loader.loadTexture(background_texture_path)
        self.map.setTexture(texture)
        self.map.reparentTo(self.screen)

    def draw_points(self):
        for location in self.locations:
            location.reparentTo(self.screen)
            location.setBin("fixed", 0)
            location.setDepthTest(False)
            location.setDepthWrite(False)

    def draw_indicator(self):
        self.indicator.reparentTo(self.screen)
        self.indicator.setBin("fixed", 0)
        self.indicator.setDepthTest(False)
        self.indicator.setDepthWrite(False)

    def draw_lines(self):
        cm = CardMaker('lines_background_node')
        cm.setFrame(-1, 1, -1, 1)
        cm_node = self.screen.attachNewNode(cm.generate())
        cm_node.setTransparency(TransparencyAttrib.MAlpha)
        cm_node.setBin('fixed', 0)
        cm_node.setColor(0, 0, 0, 0)

        linesegs = LineSegs()
        linesegs.setColor(0.0, 0.0, 0.0, 1.0)
        linesegs.setThickness(2.25)
        for location in self.locations:
            loc_x, loc_y = location.get_position()
            linesegs.moveTo(loc_x, 0.0, loc_y)
            for neighbor_id in location.get_neighbors():
                neighbor = next(self.core.find_location_by_id(neighbor_id))
                nb_x, nb_y = neighbor.get_position()
                linesegs.drawTo(nb_x, 0.0, nb_y)
                linesegs.moveTo(loc_x, 0.0, loc_y)
        line_node = linesegs.create()
        cm_node.attachNewNode(line_node)

    def show(self):
        self.screen.show()

    def hide(self):
        self.screen.hide()

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import LineSegs
from direct.gui.DirectGui import DirectFrame


class Minimap:
    def __init__(self, core):
        self.core = core
        self.image = OnscreenImage(image="resource/minimap.png", pos=(0.7, 0, -0.7), parent=self.core.render2d, scale=0.2)
        #self.image = OnscreenText(text='anyád', pos=(0, 0), scale=0.5)
        linesegs = LineSegs()
        linesegs.set_color(1, 0, 1, 0)
        linesegs.move_to(0.0, 0.0, 0.0)
        linesegs.draw_to(0.5, 0.0, 0.5)
        line_node = linesegs.create()
        self.image.attachNewNode(line_node)
        #self.line_node.create()


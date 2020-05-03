from pathlib import Path
from direct.gui.DirectGui import DirectFrame
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import LineSegs


class Minimap:
    def __init__(self, core):
        self.core = core
        self.screen = DirectFrame(frameColor=(1, 1, 1, 0))
        self.image_path = Path("resource/minimap.png")
        self.image = OnscreenImage(image="resource/minimap.png", pos=(0.7, 0.0, -0.7), scale=0.2, parent=self.core.render2d)

        linesegs = LineSegs()
        linesegs.set_color(1.0, 0.0, 0.0, 0.0)
        linesegs.move_to(0.0, 0.0, 0.0)
        linesegs.draw_to(0.5, 0.0, 0.5)
        line_node = linesegs.create()
        self.image.attachNewNode(line_node)


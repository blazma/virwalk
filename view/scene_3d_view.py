from view.view import View
from direct.gui.DirectGui import *

class Scene3DView(View):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.screen = DirectDialog(frameSize=(-0.9, 0.9, -0.9, 0.9), fadeScreen=0.4, relief=DGG.FLAT)
        scene_3d_view_label = DirectLabel(
            text="This is the 3dView scene.",
            parent=self.screen, scale=0.1, pos=(0, 0, 0.4))
        self.screen.hide()
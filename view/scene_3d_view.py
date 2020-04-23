from view.view import View
from direct.gui.DirectGui import *

class Scene3DView(View):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.screen = DirectDialog(frameSize=(-0.9, 0.9, -0.9, 0.9), fadeScreen=0.4, relief=DGG.FLAT, frameTexture="red.jpg")
        self.screen.hide()
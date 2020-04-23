from view.view import View
from direct.gui.DirectGui import *

class PauseMenuView(View):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.screen = DirectDialog(frameSize=(-0.9, 0.9, -0.9, 0.9), fadeScreen=0.4, relief=DGG.FLAT, frameTexture="blue.jpg")
        pause_view_label = DirectLabel(
            text="Do you want to continue this tour?\nIf yes, press continue,\nif you want to exit, then press quit!",
            parent=self.screen, scale=0.1, pos=(0, 0, 0.4))
        continue_button = DirectButton(text="Continue", pos=(0, 0, -0.2), parent=self.screen, scale=0.1)
        quit_button = DirectButton(text="Quit", pos=(0, 0, -0.4), parent=self.screen, scale=0.1)
        self.screen.hide()
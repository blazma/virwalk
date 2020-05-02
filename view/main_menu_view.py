from view.view import View
from direct.gui.DirectGui import *

class MainMenuView(View):
    def __init__(self, core):
        super().__init__()
        self.core = core
        #self.background = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-1, 1, -1, 1), parent=render2d)
        self.screen = DirectFrame(frameColor=(1, 1, 1, 0))
        main_view_label = DirectLabel(text="Welcome to VirWalk!\n\nChoose from the following options:", scale=0.1, pos=(0, 0, 0.4), parent=self.screen)
        start_button = DirectButton(text="Start expoloring", command=core.change_for_scene_3d_view, pos=(0, 0, -0.2), parent=self.screen, scale=0.1)
        #start_button.setTransparency(True)
        map_button = DirectButton(text="Go to the map", command=core.debug, pos=(0, 0, -0.4), parent=self.screen, scale=0.1)
        #map_button.setTransparency(True)
        quit_button = DirectButton(text="Quit", command=quit, pos=(0, 0, -0.6), parent=self.screen, scale=0.1)
        #quit_button.setTransparency(True)
        self.screen.hide()
from view.view import View
from direct.gui.DirectGui import *


class MainMenuView(View):
    BUTTON_RATIO = 431/(69*1.4)

    def __init__(self, core):
        super().__init__(core)
        self.screen = DirectFrame(frameColor=(1, 1, 1, 0), frameSize=(-1, 1, -1, 1), scale=(1.4, 1.0, 1.0),
                                  image="resource/textures/main_menu_background.png", parent=self.core.aspect2d)
        self.start_button = DirectButton(command=self.on_start_button, image="resource/textures/main_menu_start.png",
                                         pos=(0, 0, -0.2), parent=self.screen, scale=(self.BUTTON_RATIO*0.1, 1.0, 0.1), relief=None)
        self.quit_button = DirectButton(command=self.on_quit_button, pos=(0, 0, -0.6), parent=self.screen,
                                        image="resource/textures/quit.png", scale=(self.BUTTON_RATIO*0.1, 1.0, 0.1), relief=None)
        self.screen.hide()

    def __repr__(self):
        return 'main_menu_view'

    def on_start_button(self):
        self.close_view()
        self.core.set_active_view(self.core.scene_3d_view)

    def on_quit_button(self):
        quit()

    def load_view(self):
        self.screen.show()

    def close_view(self):
        self.screen.hide()

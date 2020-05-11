from view.view import View
from direct.gui.DirectGui import *


class MainMenuView(View):
    SCALING_FACTOR = 1.4
    BUTTON_ASPECT_RATIO = 431/69
    BUTTON_SCALING_FACTOR = BUTTON_ASPECT_RATIO/SCALING_FACTOR

    def __init__(self, core):
        super().__init__(core)
        paths = self.core.PATHS
        self.screen = DirectFrame(frameColor=(1, 1, 1, 0),
                                  frameSize=(-1, 1, -1, 1),
                                  scale=(self.SCALING_FACTOR, 1.0, 1.0),
                                  image=paths["MAIN_MENU_BG"],
                                  parent=self.core.aspect2d)
        self.start_button = DirectButton(command=self.on_start_button,
                                         image=paths["MAIN_MENU_START"],
                                         pos=(0, 0, -0.2),
                                         parent=self.screen,
                                         scale=(self.BUTTON_SCALING_FACTOR*0.1, 1.0, 0.1),
                                         relief=None)
        self.quit_button = DirectButton(command=self.on_quit_button,
                                        pos=(0, 0, -0.6),
                                        parent=self.screen,
                                        image=paths["MAIN_MENU_QUIT"],
                                        scale=(self.BUTTON_SCALING_FACTOR*0.1, 1.0, 0.1),
                                        relief=None)
        self.screen.hide()

    def __repr__(self):
        return 'Main Menu View'

    def on_start_button(self):
        self.close_view()
        self.core.set_active_view(self.core.scene_3d_view)

    def on_quit_button(self):
        quit()

    def load_view(self):
        self.screen.show()

    def close_view(self):
        self.screen.hide()

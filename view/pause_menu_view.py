from view.view import View
from direct.gui.DirectGui import *


class PauseMenuView(View):
    SCALING_FACTOR = 0.9
    BUTTON_ASPECT_RATIO = 431/69
    BUTTON_SCALING_FACTOR = BUTTON_ASPECT_RATIO/SCALING_FACTOR

    def __init__(self, core):
        super().__init__(core)
        paths = self.core.PATHS
        self.screen = DirectDialog(frameSize=(-self.SCALING_FACTOR, self.SCALING_FACTOR,
                                              -self.SCALING_FACTOR, self.SCALING_FACTOR),
                                   fadeScreen=0.4,
                                   relief=DGG.FLAT)
        self.pause_view_label = DirectLabel(text="Do you want to continue this tour?",
                                            parent=self.screen,
                                            scale=0.1,
                                            pos=(0, 0, 0.4))
        self.continue_button = DirectButton(command=self.on_start_button,
                                            pos=(0, 0, -0.15),
                                            image=paths["PAUSE_MENU_CONTINUE"],
                                            parent=self.screen,
                                            scale=(self.BUTTON_SCALING_FACTOR*0.1, 1.0, 0.1),
                                            relief=None)
        self.back_button = DirectButton(command=self.on_back_button,
                                        pos=(0, 0, -0.55),
                                        parent=self.screen,
                                        scale=(self.BUTTON_SCALING_FACTOR*0.1, 1.0, 0.1),
                                        image=paths["PAUSE_MENU_BACK"],
                                        relief=None)
        self.screen.hide()

    def __repr__(self):
        return 'Pause Menu View'

    def on_start_button(self):
        self.close_view()
        self.core.scene_3d_view.options_menu.wrap()
        self.core.scene_3d_view.is_pause_on = False
        self.core.set_active_view(self.core.scene_3d_view)
        self.core.scene_3d_view.set_up_controls()

    def on_back_button(self):
        self.close_view()
        self.core.scene_3d_view.close_view()
        self.core.set_active_view(self.core.main_menu_view)

    def load_view(self):
        self.screen.show()

    def close_view(self):
        self.screen.hide()

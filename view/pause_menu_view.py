from view.view import View
from direct.gui.DirectGui import *


class PauseMenuView(View):
    BUTTON_RATIO = 431/(69*0.9)

    def __init__(self, core):
        super().__init__(core)
        self.screen = DirectDialog(frameSize=(-0.9, 0.9, -0.9, 0.9), fadeScreen=0.4, relief=DGG.FLAT)
        self.pause_view_label = DirectLabel(
            text="Do you want to continue this tour?",
            parent=self.screen, scale=0.1, pos=(0, 0, 0.4))
        self.continue_button = DirectButton(command=self.on_start_button, pos=(0, 0, -0.15), image="resource/textures/pause_menu_continue.png",
                                            parent=self.screen, scale=(self.BUTTON_RATIO*0.1, 1.0, 0.1), relief=None)
        self.back_button = DirectButton(command=self.on_back_button, pos=(0, 0, -0.55), parent=self.screen, scale=(self.BUTTON_RATIO*0.1, 1.0, 0.1),
                                        image="resource/textures/pause_menu_back_to_mm.png", relief=None)
        self.screen.hide()

    def __repr__(self):
        return 'pause_menu_view'

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

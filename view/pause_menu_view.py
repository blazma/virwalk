from view.view import View
from direct.gui.DirectGui import *


class PauseMenuView(View):
    def __init__(self, core):
        super().__init__(core)
        self.screen = DirectDialog(frameSize=(-0.9, 0.9, -0.9, 0.9), fadeScreen=0.4, relief=DGG.FLAT)
        self.pause_view_label = DirectLabel(
            text="Do you want to continue this tour?\nIf yes, press continue,\nif you want to exit, then press quit!",
            parent=self.screen, scale=0.1, pos=(0, 0, 0.4))
        self.continue_button = DirectButton(text="Continue", command=self.on_start_button, pos=(0, 0, -0.2), parent=self.screen, scale=0.1)
        self.back_button = DirectButton(text="Back to the main menu", command=self.on_back_button, pos=(0, 0, -0.4), parent=self.screen, scale=0.1)
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
        self.core.set_active_view(self.core.main_menu_view)

    def load_view(self):
        self.screen.show()

    def close_view(self):
        self.screen.hide()

from view.view import View
from direct.gui.DirectGui import *


class MainMenuView(View):
    def __init__(self, core):
        super().__init__(core)
        self.screen = DirectFrame(frameColor=(1, 1, 1, 0))
        self.main_view_label = DirectLabel(text="Welcome to VirWalk!\n\nChoose from the following options:", scale=0.1, pos=(0, 0, 0.4), parent=self.screen)
        self.start_button = DirectButton(text="Start expoloring", command=self.on_start_button, pos=(0, 0, -0.2), parent=self.screen, scale=0.1)
        self.quit_button = DirectButton(text="Quit", command=self.on_quit_button, pos=(0, 0, -0.6), parent=self.screen, scale=0.1)
        self.screen.hide()

    def on_start_button(self):
        self.close_view()
        self.core.set_active_view(self.core.scene_3d_view)

    def on_quit_button(self):
        quit()

    def load_view(self):
        self.screen.show()

    def close_view(self):
        self.screen.hide()

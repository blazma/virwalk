from view.view import View
from direct.gui.DirectGui import *
from panda3d.core import TransparencyAttrib


class OptionsMenu(View):
    def __init__(self, core):
        super().__init__(core)
        self.is_minimap_hidden = False
        self.path = 'resource/textures/options.png'
        self.closed_window = DirectButton(frameColor=(0, 0, 0, 0), command=self.change_options_look, image=self.path, pos=(-1.2, 0, 0.9), scale=0.10)
        self.closed_window.hide()
        self.closed_window['state'] = DGG.NORMAL
        self.closed_window.bind(DGG.WITHIN, self.on_hover_over)
        self.closed_window.setTransparency(TransparencyAttrib.MAlpha)

        self.opened_window = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-1.5, -0.1, 0.75, 1.0))
        self.opened_window['state'] = DGG.NORMAL
        self.opened_window.setTransparency(TransparencyAttrib.MAlpha)

        self.minimap_chbx = DirectCheckButton(text='Hide minimap', pos=(-1.07, 0, 0.78), scale=0.06, command=self.check_on, parent=self.opened_window)
        self.rot_sens_slider = DirectSlider(pos=(-0.4, 0, 0.95), scale=0.2, range=(0.2, 5), value=1, pageSize=3, command=self.core.set_rot_sens, parent=self.opened_window)
        self.zoom_sens_slider = DirectSlider(pos=(-0.4, 0, 0.87), scale=0.2, range=(0.25, 4), value=1, pageSize=3, command=self.core.set_zoom_sens, parent=self.opened_window)
        self.rot_sens_lbl = DirectLabel(text='Rotation sensitivity', scale=0.07, pos=(-1.03, 0, 0.94), parent=self.opened_window)
        self.zoom_sens_lbl = DirectLabel(text='Zoom sensitivity', scale=0.072, pos=(-1.06, 0, 0.86), parent=self.opened_window)
        self.opened_window.hide()
        self.active_options = self.closed_window

    def on_hover_over(self, _):
        self.change_options_look()

    def on_hover_off(self, _):
        self.wrap()

    def check_on(self, _):
        if not self.is_minimap_hidden:
            self.core.minimap.hide()
            self.is_minimap_hidden = True
        else:
            self.core.minimap.show()
            self.is_minimap_hidden = False

    def change_options_look(self):
        self.core.scene_3d_view.is_options_on = True
        self.core.scene_3d_view.ignore_mouse()
        self.close_view()
        self.active_options = self.opened_window
        self.opened_window.bind(DGG.WITHOUT, self.on_hover_off)
        self.load_view()

    def wrap(self):
        self.close_view()
        self.active_options = self.closed_window
        self.load_view()
        self.core.scene_3d_view.is_options_on = False
        self.core.scene_3d_view.set_up_controls()

    def load_view(self):
        self.active_options.show()

    def close_view(self):
        self.active_options.hide()

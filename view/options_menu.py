from view.view import View
from direct.gui.DirectGui import *

class OptionsMenu(View):
    def __init__(self, core):
        super().__init__(core)
        self.path = 'view/options.png'
        self.closed_window = DirectButton(frameColor=(0, 0, 0, 0), command=self.change_options_look, image=self.path, pos=(-1.27, 0, 0.94), scale=0.05)
        self.closed_window.hide()
        self.opened_window = DirectFrame(frameColor=(0, 0, 0, 0), pos=(0, 0, 0)) # Unuseful, only for management purposes
        self.minimap_chbx = DirectCheckButton(text='Show minimap', pos=(-1.07, 0, 0.78), scale=0.06, command=self.check_on, parent=self.opened_window)
        self.rot_sens_slider = DirectSlider(pos=(-0.4, 0, 0.95), scale=0.2, range=(0.2, 5), value=1, pageSize=3, command=self.core.set_rot_sens, parent=self.opened_window)
        self.zoom_sens_slider = DirectSlider(pos=(-0.4, 0, 0.87), scale=0.2, range=(0.25, 4), value=1, pageSize=3, command=self.core.set_zoom_sens, parent=self.opened_window)
        self.rot_sens_lbl = DirectLabel(text='Rotation sensitivity', scale=0.07, pos=(-1.03, 0, 0.94), parent=self.opened_window)
        self.zoom_sens_lbl = DirectLabel(text='Zoom sensitivity', scale=0.072, pos=(-1.06, 0, 0.86), parent=self.opened_window)
        self.close_button = DirectButton(text='x', pos=(-0.15, 0, 0.73), scale=0.06, command=self.wrap, parent=self.opened_window)
        self.opened_window.hide()
        self.active_options = self.closed_window

    def check_on(x, y):
        #connect it with minimap release!!!
        print('Checkbox is pressed')

    def change_options_look(self):
        self.core.scene_3d_view.is_options_on = True
        self.core.scene_3d_view.ignore_mouse()
        self.close_view()
        self.active_options = self.opened_window
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
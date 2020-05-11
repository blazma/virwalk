from view.view import View
from direct.gui.DirectGui import *
from panda3d.core import TransparencyAttrib


class OptionsMenu(View):
    def __init__(self, core):
        super().__init__(core)
        self.is_minimap_hidden = False
        self.path = self.core.PATHS["OPTIONS_BUTTON"]

        # create options button and bind hover over event
        self.options_button = DirectButton(frameColor=(0, 0, 0, 0),
                                           command=self.change_options_look,
                                           image=self.path,
                                           pos=(-1.2, 0, 0.875),
                                           scale=0.10)
        self.options_button.hide()
        self.options_button['state'] = DGG.NORMAL
        self.options_button.bind(DGG.WITHIN, self.on_hover_over)
        self.options_button.setTransparency(TransparencyAttrib.MAlpha)

        # create frame appearing when user hovers over options button
        self.options_frame = DirectFrame(frameColor=(0, 0, 0, 0.5),
                                         frameSize=(-1.5, -0.1, 0.75, 1.0))
        self.options_frame['state'] = DGG.NORMAL
        self.options_frame.setTransparency(TransparencyAttrib.MAlpha)

        # define buttons, labels and sliders
        self.minimap_checkbox = DirectCheckButton(text='Hide minimap',
                                                  pos=(-1.05, 0, 0.78),
                                                  scale=0.07,
                                                  command=self.on_minimap_checkbox,
                                                  parent=self.options_frame,
                                                  relief=None)
        self.rotation_sensitivity_slider = DirectSlider(pos=(-0.4, 0, 0.95),
                                                        scale=0.2,
                                                        range=(0.2, 5),
                                                        value=1,
                                                        pageSize=3,
                                                        command=self.core.set_rotation_sensitivity,
                                                        parent=self.options_frame)
        self.zoom_sensitivity_slider = DirectSlider(pos=(-0.4, 0, 0.87),
                                                    scale=0.2,
                                                    range=(0.25, 4),
                                                    value=1,
                                                    pageSize=3,
                                                    command=self.core.set_zoom_sensitivity,
                                                    parent=self.options_frame)
        self.rotation_sensitivity_label = DirectLabel(text='Rotation sensitivity',
                                                      scale=0.07,
                                                      pos=(-1.03, 0, 0.94),
                                                      parent=self.options_frame,
                                                      relief=None)
        self.zoom_sensitivity_label = DirectLabel(text='Zoom sensitivity',
                                                  scale=0.072,
                                                  pos=(-1.06, 0, 0.86),
                                                  parent=self.options_frame,
                                                  relief=None)
        # change text color to white
        self.rotation_sensitivity_label["text_fg"] = (1, 1, 1, 1)
        self.zoom_sensitivity_label["text_fg"] = (1, 1, 1, 1)
        self.minimap_checkbox["text_fg"] = (1, 1, 1, 1)

        self.options_frame.hide()
        self.active_options = self.options_button

    def on_hover_over(self, _):
        self.change_options_look()

    def on_hover_off(self, _):
        self.wrap()

    def on_minimap_checkbox(self, _):
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
        self.active_options = self.options_frame
        self.options_frame.bind(DGG.WITHOUT, self.on_hover_off)
        self.load_view()

    def wrap(self):
        self.close_view()
        self.active_options = self.options_button
        self.load_view()
        self.core.scene_3d_view.is_options_on = False
        self.core.scene_3d_view.set_up_controls()

    def load_view(self):
        self.active_options.show()

    def close_view(self):
        self.active_options.hide()

    def get_rotation_sensitivity(self):
        return self.rotation_sensitivity_slider.getValue()

    def get_zoom_sensitivity(self):
        return self.zoom_sensitivity_slider.getValue()

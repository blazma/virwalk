from view.view import View
from direct.task import Task
from pathlib import Path
from view.minimap import Minimap
import math


class Scene3DView(View):
    def __init__(self, core):
        super().__init__(core)
        self.scene = None
        self.loader = self.core.loader
        self.render = self.core.render

        self.task = None
        self.mouse_x, self.mouse_y = 0, 0
        self.horizontal_fov = self.core.camLens.getHfov()
        self.vertical_fov = self.core.camLens.getVfov()

        # variables for zooming
        self.zoom_level = 0
        self.delta_fov = self.fov(self.zoom_level)
        self.min_fov = 10
        self.max_fov = self.fov(1/2)
        self.fov_coefficient = self.horizontal_fov/self.vertical_fov

        self.task_manager = Task.TaskManager()
        self.camera = self.core.camera
        self.location = self.core.active_location
        self.model_path = Path("resource/cylinder.egg")
        self.minimap = Minimap(self.core)
        self.is_pause_on = False
        self.set_up_controls()


    def set_up_controls(self):
        if not self.is_pause_on:
            self.core.disable_mouse()
            self.core.accept('mouse1', self.on_mouse_press)
            self.core.accept('mouse1-up', self.on_mouse_release)
            self.core.accept('wheel_up', self.on_wheel_up)
            self.core.accept('wheel_down', self.on_wheel_down)
        self.core.accept('escape', self.on_esc_button)

    def load_view(self):
        self.core.get_active_view().close_view()
        self.scene = self.loader.loadModel(self.model_path)
        active_texture = self.core.get_active_texture()
        texture_path = Path("resource/{}".format(active_texture))
        texture = self.loader.loadTexture(texture_path)
        self.scene.setTexture(texture)
        self.scene.reparentTo(self.render)
        self.scene.setScale(2.0, 2.0, 2.0)
        self.scene.setPos(self.camera.getPos())
        self.minimap.show()
        self.core.active_location.set_to_active()

    def close_view(self):
        pass

    def update_mouse_position(self):
        self.mouse_x = self.core.mouseWatcherNode.getMouseX()
        self.mouse_y = self.core.mouseWatcherNode.getMouseY()

    def update_camera_position(self):
        # field of view
        self.horizontal_fov = self.core.camLens.getHfov()
        self.vertical_fov = self.core.camLens.getVfov()

        # horizontal and vertical pan
        try:
            new_mouse_x = self.core.mouseWatcherNode.getMouseX()
            new_mouse_y = self.core.mouseWatcherNode.getMouseY()
        except AssertionError:
            new_mouse_x = self.mouse_x
            new_mouse_y = self.mouse_y

        h, p, r = self.camera.getHpr()  # Euler angles
        delta_x = (new_mouse_x - self.mouse_x)/2
        delta_y = (new_mouse_y - self.mouse_y)/2
        angle_x = self.horizontal_fov*math.asin(delta_x)
        angle_y = self.vertical_fov*math.asin(delta_y)
        min_p = self.vertical_fov/2-math.degrees(math.atan(1/2))
        max_p = -min_p

        # calculate total angle change, prevent going out of bounds
        total_angle_x = h+angle_x
        total_angle_y = p
        if min_p <= p-angle_y <= max_p:
            total_angle_y = p-angle_y

        self.camera.setHpr(total_angle_x, total_angle_y, 0)

    @staticmethod
    def fov(x):
        """
        Helper function that calculates the field of view required to fill
        the view with the entirety of an object with size x.

        :param x: size of object (normalized between 0 and 1)
        :return: FOV angle in degrees
        """
        return math.degrees(2*math.atan(x))

    def on_mouse_press(self):

        def on_mouse_task(task):
            self.update_camera_position()
            self.update_mouse_position()
            return task.again

        self.task = self.task_manager.add(on_mouse_task)
        self.update_mouse_position()

    def on_mouse_release(self):
        self.update_camera_position()
        if self.task is not None:
            self.task_manager.remove(self.task)

    def on_wheel_up(self):
        # ZOOM OUT
        _, p, _ = self.camera.getHpr()
        self.delta_fov = self.fov(self.zoom_level)
        new_vertical_fov = self.vertical_fov + self.delta_fov
        origin_endpoint_distance = math.tan(abs(math.radians(p))+math.radians(new_vertical_fov/2))
        # endpoint in this sense means the upper/lowermost point still in the frame, on the surface of the cylinder
        if origin_endpoint_distance <= 1/2:  # due to the cylinder being 1 unit tall from lowermost point to uppermost
            self.core.camLens.setFov(hfov=self.fov_coefficient * new_vertical_fov, vfov=new_vertical_fov)
            self.zoom_level += 0.01

    def on_wheel_down(self):
        # ZOOM IN
        self.delta_fov = self.fov(self.zoom_level)
        new_vertical_fov = self.vertical_fov + self.delta_fov
        if self.min_fov <= new_vertical_fov:
            self.core.camLens.setFov(hfov=self.fov_coefficient * new_vertical_fov, vfov=new_vertical_fov)
            self.zoom_level -= 0.01

    def on_esc_button(self):
        if not self.is_pause_on:
            self.is_pause_on = True
            self.core.set_active_view(self.core.pause_menu_view)
            self.core.ignore('mouse1')
            self.core.ignore('mouse1-up')
            self.core.ignore('wheel_up')
            self.core.ignore('wheel_down')
        else:
            self.is_pause_on = False
            self.core.set_active_view(self.core.scene_3d_view)
            self.set_up_controls()

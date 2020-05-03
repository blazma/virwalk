from view.view import View
from direct.task import Task
from pathlib import Path
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
        self.location = self.core.origin
        self.model_path = Path("resource/cylinder.egg")
        self.set_up_controls()

    def set_up_controls(self):
        self.core.disable_mouse()
        self.core.accept('mouse1', self.rotate_camera)
        self.core.accept('mouse1-up', self.rotate_camera_up)
        self.core.accept('wheel_up', self.increase_fov)
        self.core.accept('wheel_down', self.decrease_fov)

    def load_view(self):
        self.core.get_active_view().close_view()
        self.scene = self.loader.loadModel(self.model_path)
        texture_path = Path("resource/photo01.jpg")
        texture = self.loader.loadTexture(texture_path)
        self.scene.setTexture(texture)
        self.scene.reparentTo(self.render)
        self.scene.setScale(2.0, 2.0, 2.0)
        self.scene.setPos(self.camera.getPos())

    def close_view(self):
        pass

    def set_camera_starting_position(self):
        self.mouse_x = self.core.mouseWatcherNode.getMouseX()
        self.mouse_y = self.core.mouseWatcherNode.getMouseY()

    def set_camera_end_position(self):
        # field of view
        self.horizontal_fov = self.core.camLens.getHfov()
        self.vertical_fov = self.core.camLens.getVfov()

        # horizontal and vertical pan
        new_mouse_x = self.core.mouseWatcherNode.getMouseX()
        new_mouse_y = self.core.mouseWatcherNode.getMouseY()
        h, p, r = self.camera.getHpr()  # Euler angles
        delta_x = (new_mouse_x - self.mouse_x)/2
        delta_y = (new_mouse_y - self.mouse_y)/2
        angle_x = self.horizontal_fov*math.asin(delta_x)
        angle_y = self.vertical_fov*math.asin(delta_y)
        self.camera.setHpr(h+angle_x, p-angle_y, 0)

    def fov(self, x):
        """
        Helper function that calculates the field of view required to fill
        the view with the entirety of an object with size x.

        :param x: size of object (normalized between 0 and 1)
        :return: FOV angle in degrees
        """
        return math.degrees(2*math.atan(x))

    def update_camera(self, task):
        self.set_camera_end_position()
        self.set_camera_starting_position()
        return task.again

    def rotate_camera(self):
        self.task = self.task_manager.add(self.update_camera)
        self.set_camera_starting_position()

    def rotate_camera_up(self):
        self.set_camera_end_position()
        if self.task is not None:
            self.task_manager.remove(self.task)

    def increase_fov(self):
        self.delta_fov = self.fov(self.zoom_level)
        new_vertical_fov = self.vertical_fov + self.delta_fov
        if new_vertical_fov <= self.max_fov:
            self.core.camLens.setFov(hfov=self.fov_coefficient * new_vertical_fov, vfov=new_vertical_fov)
            self.zoom_level += 0.01

    def decrease_fov(self):
        self.delta_fov = self.fov(self.zoom_level)
        new_vertical_fov = self.vertical_fov + self.delta_fov
        if self.min_fov <= new_vertical_fov:
            self.core.camLens.setFov(hfov=self.fov_coefficient * new_vertical_fov, vfov=new_vertical_fov)
            self.zoom_level -= 0.01

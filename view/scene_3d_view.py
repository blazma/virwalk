from view.view import View
from direct.task import Task
import math


class Scene3DView(View):
    def __init__(self, core):
        super().__init__(core)
        self.inc = 0
        self.task = None
        self.mouse_x, self.mouse_y = None, None
        self.task_manager = Task.TaskManager()

        self.camera = self.core.camera
        self.location = self.core.origin
        self.model_path = "resource\cylinder.egg"
        self.core.disable_mouse()
        self.core.accept('mouse1', self.rotate_camera)
        self.core.accept('mouse1-up', self.rotate_camera_up)
        self.core.accept('wheel-up', self.increase_fov)
        self.core.accept('wheel-down', self.decrease_fov)

    def load_view(self):
        return self.core.loader.loadModel(self.model_path)

    def set_camera_starting_position(self):
        self.mouse_x = self.core.mouseWatcherNode.getMouseX()
        self.mouse_y = self.core.mouseWatcherNode.getMouseY()

    def set_camera_end_position(self):
        new_mouse_x = self.core.mouseWatcherNode.getMouseX()
        new_mouse_y = self.core.mouseWatcherNode.getMouseY()
        h, p, r = self.camera.getHpr()
        delta_x = (new_mouse_x - self.mouse_x)/2
        delta_y = (new_mouse_y - self.mouse_y)/2
        field_of_view = self.core.camLens.getHfov()
        angle = field_of_view*math.asin(delta_x)
        #self.camera.setHpr(h+angle, 0, 0)
        self.core.camLens.setFov(field_of_view+180*math.asin(delta_y)/math.pi)
        print(self.core.camLens.getHfov())

    def update_camera(self, task):
        self.set_camera_end_position()
        self.set_camera_starting_position()
        return task.again

    def rotate_camera(self):
        self.task = self.task_manager.add(self.update_camera)
        self.set_camera_starting_position()

    def rotate_camera_up(self):
        self.set_camera_end_position()
        self.task_manager.remove(self.task)

    def increase_fov(self):
        field_of_view = self.core.camLens.getHfov()
        print("fel")
        self.camera.node().getLens().setHFov(120)

    def decrease_fov(self):
        field_of_view = self.core.camLens.getFov()
        print("le")
        self.camera.node().getLens().setHFov(60)

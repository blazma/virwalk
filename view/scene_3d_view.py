from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerQueue
from panda3d.core import CollisionNode
from panda3d.core import CollisionRay
from panda3d.core import GeomNode
from view.view import View
from direct.task import Task
import math


class Scene3DView(View):
    def __init__(self, core):
        super().__init__(core)
        self.scene = self.core.scene_3d_model
        self.loader = self.core.loader
        self.render = self.core.render
        self.minimap = self.core.minimap

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

        # collision detector TODO: find a new location for
        self.collision_traverser = CollisionTraverser()
        self.collision_handler = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.core.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.collision_traverser.addCollider(self.pickerNP, self.collision_handler)

        self.task_manager = Task.TaskManager()
        self.camera = self.core.camera
        self.location = self.core.active_location
        self.indicator = self.core.indicator
        self.is_pause_on = False

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
        texture = self.core.get_active_location().get_texture()
        self.scene.setTexture(texture)
        self.scene.reparentTo(self.render)
        self.scene.setScale(2.0, 2.0, 2.0)
        self.scene.setPos(self.camera.getPos())
        self.core.active_location.set_to_active()
        self.load_neighbor_markers()
        self.minimap.show()
        self.set_up_controls()

    def close_view(self):
        pass

    def load_neighbor_markers(self):
        for neighbor_id in self.location.get_neighbors():
            marker_center_node = self.scene.attachNewNode("{}_marker_center_node".format(neighbor_id))
            angle, marker_model = self.location.neighbor_markers[neighbor_id]
            marker_model.reparentTo(marker_center_node)
            marker_center_node.setH(angle)
            marker_model.show()

    def update_indicator_angle(self, delta_angle):
        current_angle = self.indicator.getR()
        self.indicator.setR(current_angle - delta_angle)

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
        self.update_indicator_angle(angle_x)

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

        mpos = self.core.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(self.core.camNode, mpos.getX(), mpos.getY())
        self.collision_traverser.traverse(self.render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        if self.collision_handler.getNumEntries() > 0:
            # This is so we get the closest object.
            self.collision_handler.sortEntries()
            pickedObj = self.collision_handler.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetPythonTag('marker_tag')
            if not pickedObj.isEmpty():
                picked_location = self.core.find_location_by_marker(pickedObj)
                self.change_location(picked_location)

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

    def change_location(self, new_location):
        active_location = self.core.get_active_location()
        markers = active_location.get_markers()
        for neighbor_id in markers:
            angle, model = markers[neighbor_id]
            model.hide()
        self.core.set_active_location(new_location)
        self.location = self.core.active_location
        self.load_neighbor_markers()
        loc_x, loc_y = self.location.get_position()
        self.indicator.setPos(loc_x, 0, loc_y)

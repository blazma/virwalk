from direct.actor.Actor import Actor


class Location(Actor):
    PATHS = {
        "LOCATION_MARKER_MODEL": "resource/models/arrow.egg",
        "MINIMAP_POINT_MODEL": "resource/models/point.egg"
    }
    SCALE = 0.065

    def __init__(self, id, x, y, neighbors, texture):
        super().__init__(self.PATHS["MINIMAP_POINT_MODEL"])
        self.id = id
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.neighbor_markers = {}
        self.texture = texture
        self.setPos(self.x, 0, self.y)
        self.setColor(0.0, 0.0, 0.0, 0.0)
        self.setScale(self.SCALE, self.SCALE, self.SCALE)
        self.is_active = False

    def add_neighbor_marker(self, neighbor, marker_angle, marker_texture):
        marker_model = Actor(self.PATHS["LOCATION_MARKER_MODEL"])
        marker_model.setPythonTag('marker_tag', self.id*10+neighbor.id)
        marker_model.setTexture(marker_texture)
        marker_model.setScale(1.0, 1.0, 1.0)
        if isinstance(neighbor, Location):
            self.neighbor_markers[neighbor.id] = (marker_angle, marker_model)
        else:
            self.neighbor_markers[neighbor] = (marker_angle, marker_model)

    def set_to_active(self):
        self.is_active = True
        self.setColor(1.0, 0.0, 0.0, 0.0)

    def set_to_inactive(self):
        self.is_active = False
        self.setColor(0.0, 0.0, 0.0, 0.0)

    def get_neighbors(self):
        return self.neighbors

    def get_markers(self):
        return self.neighbor_markers

    def get_texture(self):
        return self.texture

    def get_position(self):
        return self.x, self.y

from direct.actor import Actor


class Location(Actor.Actor):
    SCALE = 0.065
    MODEL_PATH = "resource/point.egg"

    def __init__(self, id, x, y, neighbors, texture):
        super().__init__()#self.MODEL_PATH)
        self.id = id
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.texture = texture
        self.setPos(self.x, 0, self.y)
        self.setColor(0.0, 0.0, 0.0, 0.0)
        self.setScale(self.SCALE, self.SCALE, self.SCALE)
        self.is_active = False

    def set_to_active(self):
        self.is_active = True
        self.setColor(1.0, 0.0, 0.0, 0.0)

    def set_to_inactive(self):
        self.is_active = False
        self.setColor(0.0, 0.0, 0.0, 0.0)

    def get_neighbors(self):
        return self.neighbors

    def get_texture(self):
        return self.texture

    def get_position(self):
        return self.x, self.y

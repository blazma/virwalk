from model.core import Core
from model.logging import Logger


class Virwalk():
    def __init__(self):
        Logger.clear_logs()
        self.core = Core()

    def run(self):
        self.core.run()


if __name__ == '__main__':
    app = Virwalk()
    app.run()

from model.core import Core
from view.main_menu_view import MainMenuView


class Virwalk:
    def __init__(self):
        self.core = Core()

    def run(self):
        self.core.set_view(MainMenuView)
        self.core.run()


if __name__ == '__main__':
    app = Virwalk()
    app.run()

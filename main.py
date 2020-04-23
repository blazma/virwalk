from model.core import Core

class Virwalk():
    def __init__(self):
        self.core = Core()

    def run(self):
        self.core.run()

if __name__ == '__main__':
    app = Virwalk()
    app.run()

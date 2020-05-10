from model.core import Core
from model.logging import Logger
import argparse


class Virwalk():
    def __init__(self, args):
        Logger.DEBUGGER = args.debug
        Logger.clear_logs()
        self.core = Core()

    def run(self):
        self.core.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-d", type=int, default=0, help="Debug mode ON: 1. (Runtime of different "
                                                                   "functions)")
    args = parser.parse_args()

    app = Virwalk(args)
    app.run()




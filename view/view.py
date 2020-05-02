from abc import ABC
from abc import abstractmethod


class View(ABC):
    def __init__(self, core):
        self.core = core

    @abstractmethod
    def load_view(self):
        raise NotImplementedError

    @abstractmethod
    def close_view(self):
        raise NotImplementedError

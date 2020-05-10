import unittest
from unittest.mock import patch
import random
from model.core import Core
from view.scene_3d_view import Scene3DView


class TestCore(unittest.TestCase):
    @patch('__main__.main.')
    def test_texture_change_after_location_change(self, main):
        pass


if __name__ == "__main__":
    unittest.main()

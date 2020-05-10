import unittest
from unittest.mock import patch
from view.scene_3d_view import Scene3DView


class TestScene3DView(unittest.TestCase):
    @patch('view.scene_3d_view.Scene3DView.core')
    def test_change_location(self, MockScene3DView):
        
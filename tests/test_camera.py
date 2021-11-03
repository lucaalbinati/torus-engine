import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, "{}/..".format(dir_path))

import math
import pytest
import numpy as np
from utils import normalize_vector
from scene.camera import Camera
from scene.move import Move

ORIGIN = np.array([0, 0, 0])
NO_HORIZONTAL_ROTATION = 0

@pytest.mark.parametrize("observer,point_to_fix,horizontal_rotation,normal,up,horizontal",
    [
        (np.array([1, 0, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, np.array([-1, 0, 0]), np.array([0, 0, 1]), np.array([0, 1, 0])),
        (np.array([0, 1, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, np.array([0, -1, 0]), np.array([0, 0, 1]), np.array([-1, 0, 0])),
        (np.array([0, 0, 1]), ORIGIN, NO_HORIZONTAL_ROTATION, np.array([0, 0, -1]), np.array([-1, 0, 0]), np.array([0, 1, 0])),
        (np.array([1, 1, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, normalize_vector(np.array([-1, -1, 0])), normalize_vector(np.array([0, 0, 1])), normalize_vector(np.array([-1, 1, 0]))),
        (np.array([1, 1, 0]), np.array([0, 1, 0]), NO_HORIZONTAL_ROTATION, normalize_vector(np.array([-1, 0, 0])), normalize_vector(np.array([0, 0, 1])), normalize_vector(np.array([0, 1, 0]))),
        (np.array([1, 0, 0]), ORIGIN, math.pi/2, normalize_vector(np.array([-1, 0, 0])), normalize_vector(np.array([0, 1, 0])), normalize_vector(np.array([0, 0, -1]))),
        (np.array([1, 0, 0]), ORIGIN, math.pi/4, normalize_vector(np.array([-1, 0, 0])), normalize_vector(np.array([0, 1, 1])), normalize_vector(np.array([0, 1, -1]))),
        (np.array([1, 1, 0]), ORIGIN, math.pi/4, normalize_vector(np.array([-1, -1, 0])), normalize_vector(np.array([-1, 1, math.sqrt(2)])), normalize_vector(np.array([-1, 1, -math.sqrt(2)]))),
        (np.array([0, 0, 1]), ORIGIN, math.pi, normalize_vector(np.array([0, 0, -1])), normalize_vector(np.array([1, 0, 0])), normalize_vector(np.array([0, -1, 0]))),
        (np.array([1, 1, 2]), np.array([-0.5, 2, 0]), math.pi/4, np.array([-0.55708601, 0.37139068, -0.74278135]), np.array([-0.04478195, 0.87969122, 0.47343208]), np.array([0.82924649, 0.29700559, -0.47343208]))
    ]
)
def test_camera_orientation(observer, point_to_fix, horizontal_rotation, normal, up, horizontal):
    camera = Camera(observer=observer, point_to_fix=point_to_fix, horizontal_rotation=horizontal_rotation)
    assert np.allclose(camera.plane.normal, normal)
    assert np.allclose(camera.plane.up, up)
    assert np.allclose(camera.plane.horizontal, horizontal)

@pytest.mark.parametrize("observer,point_to_fix,horizontal_rotation,move_sequence,new_camera_point",
    [
        (np.array([2, 0, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.LEFT, Move.LEFT, Move.RIGHT, Move.RIGHT], np.array([2, 0, 0])),
        (np.array([2, 5, -1]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.UP, Move.UP, Move.DOWN, Move.DOWN], np.array([2, 5, -1])),
        (np.array([0, 2, 3]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.LEFT, Move.LEFT, Move.RIGHT, Move.LEFT, Move.RIGHT, Move.RIGHT], np.array([0, 2, 3])),
        (np.array([1, 0, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.LEFT, Move.UP, Move.RIGHT, Move.DOWN], np.array([1, 0, 0]))
    ]
)
def test_camera_movement(observer, point_to_fix, horizontal_rotation, move_sequence, new_camera_point):
    camera = Camera(observer=observer, point_to_fix=point_to_fix, horizontal_rotation=horizontal_rotation)
    for move in move_sequence:
        camera.move(move)
    assert np.allclose(camera.camera_point, new_camera_point)
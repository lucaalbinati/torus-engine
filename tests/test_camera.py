import math
import pytest
import numpy as np
from engine.utils import normalize_vector
from engine.camera import Camera
from engine.move import Move

ORIGIN = np.array([0, 0, 0])
NO_HORIZONTAL_ROTATION = 0
DEFAULT_ATOL = 1.e-8

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

@pytest.mark.parametrize("observer,point_to_fix,horizontal_rotation,move_sequence,expected_camera_point,atol",
    [
        (np.array([2, 0, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.LEFT, Move.LEFT, Move.RIGHT, Move.RIGHT], np.array([2, 0, 0]), DEFAULT_ATOL),
        (np.array([2, 5, -1]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.UP, Move.UP, Move.DOWN, Move.DOWN], np.array([2, 5, -1]), DEFAULT_ATOL),
        (np.array([1, 0, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.LEFT, Move.LEFT, Move.RIGHT, Move.LEFT, Move.RIGHT, Move.RIGHT], np.array([1, 0, 0]), DEFAULT_ATOL),
        (np.array([1, 0, 0]), ORIGIN, NO_HORIZONTAL_ROTATION, [Move.LEFT, Move.UP, Move.RIGHT, Move.DOWN], np.array([1, 0, 0]), 1.e-2)
    ]
)
def test_camera_movement(observer, point_to_fix, horizontal_rotation, move_sequence, expected_camera_point, atol):
    camera = Camera(observer=observer, point_to_fix=point_to_fix, horizontal_rotation=horizontal_rotation)
    prev_camera_point = camera.camera_point
    for move in move_sequence:
        camera.move(move)
        # verify that the angle between the two vectors is in line with the angle by which we rotated
        assert np.isclose(np.dot(normalize_vector(prev_camera_point), normalize_vector(camera.camera_point)), camera.cos_increment)
        prev_camera_point = camera.camera_point
    # verify that the final position of the camera is what we expected
    assert np.allclose(camera.camera_point, expected_camera_point, atol=atol)
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, "{}/..".format(dir_path))
import math
import numpy as np
from utils import normalize_vector
from main import Camera

def camera_y_0_test():
	observer = np.array([1, 0, 0])
	camera = Camera(observer)
	assert(np.allclose(camera.plane.normal, np.array([-1, 0, 0])))
	assert(np.allclose(camera.plane.up, np.array([0, 0, 1])))
	assert(np.allclose(camera.plane.horizontal, np.array([0, 1, 0])))
	print("camera_y_0_test successful")

def camera_y_not_0_test():
	observer = np.array([1, 1, 0])
	camera = Camera(observer)
	assert(np.allclose(camera.plane.normal, normalize_vector(np.array([-1, -1, 0]))))
	assert(np.allclose(camera.plane.up, normalize_vector(np.array([0, 0, 1]))))
	assert(np.allclose(camera.plane.horizontal, normalize_vector(np.array([-1, 1, 0]))))
	print("camera_y_not_0_test successful")

def camera_point_to_fix_test():
	observer = np.array([1, 1, 0])
	point_to_fix = np.array([0, 1, 0])
	camera = Camera(observer, point_to_fix=point_to_fix)
	assert(np.allclose(camera.plane.normal, normalize_vector(np.array([-1, 0, 0]))))
	assert(np.allclose(camera.plane.up, normalize_vector(np.array([0, 0, 1]))))
	assert(np.allclose(camera.plane.horizontal, normalize_vector(np.array([0, 1, 0]))))
	print("camera_point_to_fix_test successful")

def camera_rotation_test():
	observer = np.array([1, 0, 0])
	camera = Camera(observer, horizontal_rotation=(math.pi/2))
	assert(np.allclose(camera.plane.normal, normalize_vector(np.array([-1, 0, 0]))))
	assert(np.allclose(camera.plane.up, normalize_vector(np.array([0, 1, 0]))))
	assert(np.allclose(camera.plane.horizontal, normalize_vector(np.array([0, 0, -1]))))
	print("camera_rotation_test successful")

def camera_rotation_2_test():
	observer = np.array([1, 0, 0])
	camera = Camera(observer, horizontal_rotation=(math.pi/4))
	assert(np.allclose(camera.plane.normal, normalize_vector(np.array([-1, 0, 0]))))
	assert(np.allclose(camera.plane.up, normalize_vector(np.array([0, 1, 1]))))
	assert(np.allclose(camera.plane.horizontal, normalize_vector(np.array([0, 1, -1]))))
	print("camera_rotation_2_test successful")

def camera_rotation_3_test():
	observer = np.array([1, 1, 0])
	camera = Camera(observer, horizontal_rotation=(math.pi/4))
	assert(np.allclose(camera.plane.normal, normalize_vector(np.array([-1, -1, 0]))))
	assert(np.allclose(camera.plane.up, normalize_vector(np.array([-1, 1, math.sqrt(2)]))))
	assert(np.allclose(camera.plane.horizontal, normalize_vector(np.array([-1, 1, -math.sqrt(2)]))))
	print("camera_rotation_3_test successful")

def camera_complete_test():
	observer = np.array([1, 1, 2])
	point_to_fix = np.array([-0.5, 2, 0])
	camera = Camera(observer, point_to_fix=point_to_fix, horizontal_rotation=(math.pi/4))
	assert(np.allclose(camera.plane.normal, np.array([-0.55708601, 0.37139068, -0.74278135])))
	assert(np.allclose(camera.plane.up, np.array([-0.04478195, 0.87969122, 0.47343208])))
	assert(np.allclose(camera.plane.horizontal, np.array([0.82924649, 0.29700559, -0.47343208])))
	print("camera_rotation_3_test successful")

camera_y_0_test()
camera_y_not_0_test()
camera_point_to_fix_test()
camera_rotation_test()
camera_rotation_2_test()
camera_rotation_3_test()
camera_complete_test()



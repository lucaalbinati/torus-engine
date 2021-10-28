import os
import sys
import numpy as np
from pathlib import Path

PYTHON_EXTENSION = ".py"

brightness_char_zero = " "
brightness_chars_dict = {
	(0, 1): ".",
	(1, 5): ",",
	(5, 10): "-",
	(10, 15): "~",
	(15, 20): ":",
	(20, 25): ";",
	(25, 30): "=",
	(30, 35): "!",
	(35, 40): "*",
	(40, 45): "#",
	(45, 50): "$",
	(50, sys.maxsize): "@"
}

def get_brightness_char(brightness):
	if brightness == 0:
		return brightness_char_zero
	else:
		for (lower, upper), char in brightness_chars_dict.items():
			if lower <= brightness and brightness < upper:
				return char

def normalize_vector(vector):
	vector = np.array(vector)
	norm = np.linalg.norm(vector)
	if norm == 0:
		return vector
	else:
		return vector / norm

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def rotate(rotation_matrix_func, theta, points, normals):
		points = np.transpose(points)
		normals = np.transpose(normals)
		rotation_matrix = rotation_matrix_func(theta)

		if len(rotation_matrix.shape) != 2 or rotation_matrix.shape[1] != points.shape[0]:
			raise Exception("Rotation matrix must have the same number of columns as the number of dimensions, instead got {} and {}".format(rotation_matrix.shape, points.shape))
		
		points = np.transpose(np.dot(rotation_matrix, points))
		normals = np.transpose(np.dot(rotation_matrix, normals))

		return points, normals

def list_of_all_objects():
	parent_dir = Path(os.path.realpath(__file__)).parent
	objects_dir = "{}/{}".format(parent_dir, "objects")
	return [f[:-len(PYTHON_EXTENSION)] for f in os.listdir(objects_dir) if os.path.isfile(os.path.join(objects_dir, f)) and f.endswith(PYTHON_EXTENSION)]
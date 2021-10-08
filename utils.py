import os
import sys
import numpy as np

brightness_char_zero = " "
brightness_chars_dict = {
	(0, 1): ".",
	(1, 7): "?",
	(7, 14): "X",
	(14, 20): "#",
	(20, 26): "M",
	(26, 32): "&",
	(32, 37): "%",
	(37, 42): "@",
	(42, sys.maxsize): "$"
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
			raise Exception("Rotation matrix must have the same number of columns as the number of dimensions, instead got {} and {}".format(rotation_matrix.shape, self.points.shape))
		
		points = np.transpose(np.dot(rotation_matrix, points))
		normals = np.transpose(np.dot(rotation_matrix, normals))

		return points, normals
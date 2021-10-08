import numpy as np
from utils import normalize_vector, rotate

class Line:
	def __init__(self, distance_to_origin=5, step=0.01):
		self.distance_to_origin = distance_to_origin
		self.step = step
		self.position_along_axis = [position for position in np.arange(-self.distance_to_origin, self.distance_to_origin, self.step)]
		self.points = np.transpose([self.point_equation(position) for position in self.position_along_axis])
		self.normals = np.transpose([self.normal_equation(position) for position in self.position_along_axis])

	def point_equation(self, step):
		return np.array([
				0,
				0,
				step
			])

	def normal_equation(self, step):
		return normalize_vector(np.array([
				1,
				0,
				0
			]))

	def rotate(self, rotation_matrix_func, theta):
		self.points, self.normals = rotate(rotation_matrix_func, theta, self.points, self.normals)
import math
import numpy as np


class Torus:
	def __init__(self, R, r):
		self.R = R
		self.r = r
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / 100)
		self.phis = np.arange(0, 2 * math.pi, 2 * math.pi / 100)
		self.__update_points()

	def __update_points(self):
		new_points = []
		for theta in self.thetas:
			for phi in self.phis:
				new_point_x = self.R * math.cos(theta) + r * math.cos(phi)
				new_point_y = self.R * math.sin(theta) + r * math.cos(phi)
				new_point_z = self.r * math.sin(phi)
				new_point = (new_point_x, new_point_y, new_point_z)
				new_points.append(new_point)
		self.points = new_points


if __name__ == "__main__":
	print("hello")

	R = 1
	r = 0.2

	torus = Torus(R, r)

	points = torus.points
	print(len(points))
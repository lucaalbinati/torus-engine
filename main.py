import math
import numpy as np


class Torus:
	def __init__(self, R, r):
		self.R = R
		self.r = r
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / 100)
		self.phis = np.arange(0, 2 * math.pi, 2 * math.pi / 100)
		self.update()

	def update(self):
		new_points = []
		for theta in self.thetas:
			for phi in self.phis:
				new_point_x = self.R * math.cos(theta) + r * math.cos(phi)
				new_point_y = self.R * math.sin(theta) + r * math.cos(phi)
				new_point_z = self.r * math.sin(phi)
				new_point = (new_point_x, new_point_y, new_point_z)
				new_points.append(new_point)
		self.points = new_points

	def get_border_cube(self):
		x_values = list(map(lambda p: p[0], self.points))
		y_values = list(map(lambda p: p[1], self.points))
		z_values = list(map(lambda p: p[2], self.points))

		x_min = min(x_values)
		x_max = max(x_values)
		y_min = min(y_values)
		y_max = max(y_values)
		z_min = min(z_values)
		z_max = max(z_values)

		return [(x_min, y_min, z_min), (x_max, y_max, z_max)]

	def center_of_gravity(self):
		border_cube = self.get_border_cube()
		x_avg = np.average([border_cube[0][0], border_cube[1][0]])
		y_avg = np.average([border_cube[0][1], border_cube[1][1]])
		z_avg = np.average([border_cube[0][2], border_cube[1][2]])
		return (x_avg, y_avg, z_avg)


class Plane:
	def __init__(self, normal, p0):
		self.normal = normal
		self.p0 = p0
		self.PIXEL_WIDTH = 80
		self.PIXEL_HEIGHT = 30

class Scene:
	def __init__(self, obj, light_source, observer):
		self.obj = obj
		self.light_source = light_source
		self.observer = observer
		self.plane = self.__compute_plane()

	def __compute_plane(self):
		obj_center = self.obj.center_of_gravity()
		center_to_observer_vector = np.array(self.observer) - np.array(obj_center)
		plane_normal = self.__normalize_vector(center_to_observer_vector)
		p0 = np.average([obj_center[0] + self.observer[0]])
		return Plane(plane_normal, p0)

	def __normalize_vector(self, vector):
		vector = np.array(vector)
		norm = np.linalg.norm(vector)
		if norm == 0:
			return vector
		else:
			return vector / norm

if __name__ == "__main__":
	R = 1
	r = 0.2

	torus = Torus(R, r)
	light_source = (2 * R, 2 * R, 2 * R)
	observer = (3 * R, 0, 0)
	scene = Scene(torus, light_source, observer)








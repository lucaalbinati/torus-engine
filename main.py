import math
import numpy as np


def normalize_vector(vector):
		vector = np.array(vector)
		norm = np.linalg.norm(vector)
		if norm == 0:
			return vector
		else:
			return vector / norm

class Torus:
	def __init__(self, R, r, theta_step=10, phi_step=10):
		self.R = R
		self.r = r
		self.theta_step = theta_step
		self.phi_step = phi_step
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / self.theta_step)
		self.phis = np.arange(0, 2 * math.pi, 2 * math.pi / self.phi_step)
		self.update()

	def update(self):
		new_points = []
		new_normals = []
		for theta in self.thetas:
			for phi in self.phis:
				new_point_x = self.R * math.cos(theta) + r * math.cos(phi)
				new_point_y = self.R * math.sin(theta) + r * math.cos(phi)
				new_point_z = self.r * math.sin(phi)
				new_point = (new_point_x, new_point_y, new_point_z)
				new_points.append(new_point)
				new_normal = (r * math.cos(phi), r * math.cos(phi), new_point_z)
				new_normals.append(new_normal)
		self.points = new_points
		self.normals = new_normals

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
	def __init__(self, normal, up, p0, aspect_ratio=16/9, height=0.5, nb_pixel_height=45):
		self.normal = normalize_vector(normal)
		self.up = normalize_vector(up)
		self.horizontal = np.cross(self.normal, self.up)
		self.p0 = p0
		self.aspect_ratio = aspect_ratio
		self.height = height
		self.width = self.height * self.aspect_ratio
		self.nb_pixel_height = nb_pixel_height
		self.nb_pixel_width = math.ceil(self.nb_pixel_height * self.aspect_ratio)
		self.pixel_incr = self.width / self.nb_pixel_width

	@staticmethod
	def compute_plane(observer, obj, up, camera_observer_distance=1):
		obj_center = obj.center_of_gravity()
		observer_to_center_vector = np.array(obj_center) - np.array(observer)
		normal = normalize_vector(observer_to_center_vector)
		p0 = observer + camera_observer_distance * normal
		up = normalize_vector(up)
		return Plane(normal, up, p0)

	def find_intersection(self, vector_start, vector):
		l0 = vector_start
		l = vector

		# d = [(p0-l0) * n] / [n * l]
		p0l0 = np.array(self.p0) - np.array(l0)
		top = np.dot(p0l0, self.normal)
		bottom = np.dot(self.normal, l)
		d = top / bottom

		# intersection point
		p = l0 + l * d
		return p

	def clip_points_to_pixels(self, intersections_on_plane):	
		top_left_corner = self.p0 - (self.width / 2) * self.horizontal + (self.height / 2) * self.up

		grid_points = {}

		for h in range(self.nb_pixel_height):
			h_incr = - self.pixel_incr * h
			for w in range(self.nb_pixel_width):
				w_incr = self.pixel_incr * w

				point = top_left_corner + w_incr * self.horizontal + h_incr * self.up

				i = h * self.nb_pixel_width + w
				grid_points[i] = (point, 0, 0)

		#for i, (point, _, _) in grid_points.items():
		#	print("{}: {}".format(i, point))

		# find a way to clip each intersection point to the grid (ideally without having to compute [#grid_points * #intersection_points] distances)
		for (intersection_point, depth, brightness) in intersections_on_plane:
			grid_position_x = int((intersection_point[0] - top_left_corner[0]) / self.nb_pixel_width)
			grid_position_y = int((intersection_point[1] - top_left_corner[1]) / self.nb_pixel_height)
			grid_position = grid_position_y * self.nb_pixel_width + grid_position_x
			if grid_position in grid_points:
				grid_points[grid_position] = (intersection_point, depth, brightness)

		return grid_points

class Scene:
	def __init__(self, obj, light_source, observer, camera_plane):
		self.obj = obj
		self.light_source = light_source
		self.observer = observer
		self.camera_plane = camera_plane

	def __compute_illumination(self):
		self.brightnesses = []
		for point, normal in zip(self.obj.points, self.obj.normals):
			observer_to_point_vector = np.array(point) - np.array(self.observer)
			point_to_light_vector = np.array(point) - np.array(self.light_source)
			brightness = np.dot(observer_to_point_vector, point_to_light_vector)
			direction = np.dot(normal, observer_to_point_vector)
			if direction <= 0:
				brightness = 0
			self.brightnesses.append(brightness)

	def __compute_intersections_on_plane(self):
		intersections_on_plane = []
		for point, brightness in zip(self.obj.points, self.brightnesses):
			observer_to_point_vector = np.array(point) - np.array(self.observer)
			distance_to_point = np.linalg.norm(observer_to_point_vector)
			intersection_on_plane = self.camera_plane.find_intersection(self.observer, observer_to_point_vector)
			intersections_on_plane.append((intersection_on_plane, distance_to_point, brightness))
		return intersections_on_plane

	def show(self):
		self.obj.update()
		self.__compute_illumination()
		intersections_on_plane = self.__compute_intersections_on_plane()
		
		#for point, distance_to_point, brightness in intersections_on_plane:
		#	print("{}: {}, {}".format(point, distance_to_point, brightness))

		intersections_on_plane = self.camera_plane.clip_points_to_pixels(intersections_on_plane)
		# sort first by i (see #Plane::clip_points_to_pixels) and then by depth (in case there are several intersection points at the same i)
		#intersections_on_plane = sorted(intersections_on_plane, key=lambda elem: (elem[0], elem[1]))

		#for i, (intersection_point, depth, brightness) in intersections_on_plane.items():
		#	print("{}: {}, {}, {}".format(i, intersection_point, depth, brightness))
		


if __name__ == "__main__":
	R = 1
	r = 0.2

	torus = Torus(R, r)
	light_source = np.array([3 * R, 0, 0])
	observer = np.array([3 * R, 1, 0])
	camera_plane = Plane.compute_plane(observer, torus, up=np.array([0, 0, 1]))
	scene = Scene(torus, light_source, observer, camera_plane)

	scene.show()

	



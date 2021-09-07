import sys
import math
import numpy as np


def normalize_vector(vector):
		vector = np.array(vector)
		norm = np.linalg.norm(vector)
		if norm == 0:
			return vector
		else:
			return vector / norm


class Line:
	def __init__(self, distance_to_origin=5, step=0.01):
		self.distance_to_origin = distance_to_origin
		self.step = step
		self.position_along_axis = [position for position in np.arange(-self.distance_to_origin, self.distance_to_origin, self.step)]
		self.points = [self.point_equation(position) for position in self.position_along_axis]
		self.normals = [self.normal_equation(position) for position in self.position_along_axis]

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

	def contains_point(self, point):
		return False


class Sphere:
	def __init__(self, R, theta_step=200, phi_step=200):
		self.R = R
		self.r = r
		self.theta_step = theta_step
		self.phi_step = phi_step
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / self.theta_step)
		self.phis = np.arange(0, math.pi, math.pi / self.phi_step)
		self.points = [self.point_equation(theta, phi) for theta in self.thetas for phi in self.phis]
		self.normals = [self.normal_equation(theta, phi) for theta in self.thetas for phi in self.phis]

	def point_equation(self, theta, phi):
		return np.array([
				self.R * math.cos(theta) * math.sin(phi),
				self.R * math.sin(theta) * math.sin(phi),
				self.R * math.cos(phi)
			])

	def normal_equation(self, theta, phi):
		return normalize_vector(np.array([
				math.cos(theta) * math.sin(phi),
				math.sin(theta) * math.sin(phi),
				math.cos(phi)
			]))

	def contains_point(self, point):
		x, y, z = point[0], point[1], point[2]
		return (x**2 + y**2 + z**2) <= self.R

class Torus:
	def __init__(self, R, r, theta_step=100, phi_step=100):
		self.R = R
		self.r = r
		self.theta_step = theta_step
		self.phi_step = phi_step
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / self.theta_step)
		self.phis = np.arange(0, 2 * math.pi, 2 * math.pi / self.phi_step)
		self.points = [self.point_equation(theta, phi) for theta in self.thetas for phi in self.phis]
		self.normals = [self.normal_equation(theta, phi) for theta in self.thetas for phi in self.phis]
		
	def point_equation(self, theta, phi):
		return np.array([
				self.R * math.cos(theta) + r * math.cos(phi),
				self.R * math.sin(theta) + r * math.cos(phi),
				self.r * math.sin(phi)
			])

	def normal_equation(self, theta, phi):
		return normalize_vector(np.array([
				math.cos(phi),
				math.cos(phi),
				math.sin(phi)
			]))

	def contains_point(self, point):
		x, y, z = point[0], point[1], point[2]
		contains = True
		contains = contains and (self.R - self.r <= abs(x) <= self.R + self.r)
		contains = contains and (self.R - self.r <= abs(y) <= self.R + self.r)
		contains = contains and (0 <= abs(z) <= self.r)
		return contains


class Plane:
	# FIXME and maybe change how init works by not giving a "up" vector, but instead a degree of rotation, [0-360]

	def __init__(self, normal, up, p0, aspect_ratio=32/9, height=0.5, nb_pixel_height=64):
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
	def compute_p0(observer, normal, camera_observer_distance=1):
		return observer + camera_observer_distance * normal

	# FIXME false -> have to ensure that normal dot up = 0
	# @staticmethod
	# def compute_plane(observer, obj, up, camera_observer_distance=1):
	# 	obj_center = obj.center_of_gravity()
	# 	observer_to_center_vector = np.array(obj_center) - np.array(observer)
	# 	normal = normalize_vector(observer_to_center_vector)
	# 	p0 = observer + camera_observer_distance * normal
	# 	up = normalize_vector(up)
	# 	return Plane(normal, up, p0)

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
				grid_points[i] = (point, sys.maxsize, 0)

		# find a way to clip each intersection point to the grid (ideally without having to compute [#grid_points * #intersection_points] distances)
		for (intersection_point, depth, brightness) in intersections_on_plane:
			tlc_to_intersection_point = intersection_point - top_left_corner
			horizontal_shift = np.dot(self.horizontal, tlc_to_intersection_point)
			vertical_shift = np.dot(self.up, tlc_to_intersection_point)
			grid_position_w = int(horizontal_shift / self.pixel_incr)
			grid_position_h = int(- vertical_shift / self.pixel_incr)
			grid_position = grid_position_h * self.nb_pixel_width + grid_position_w
			if grid_position in grid_points:
				# replace the point if it is closer to the observer
				if depth < grid_points[grid_position][1]:
					grid_points[grid_position] = (intersection_point, depth, brightness)

		return grid_points

class Scene:
	def __init__(self, obj, light_source, observer, camera_plane, brightness_chars=" :?X#M&%@$"):
		# TODO add possiblity for multiple objects
		self.obj = obj
		self.light_source = light_source
		self.observer = observer
		self.camera_plane = camera_plane
		self.brightness_chars = brightness_chars

	def __compute_illumination(self):
		self.brightnesses = []
		for point, normal in zip(self.obj.points, self.obj.normals):
			observer_to_point_vector = np.array(point) - np.array(self.observer)
			point_to_light_vector = np.array(point) - np.array(self.light_source)
			brightness = np.dot(observer_to_point_vector, point_to_light_vector)
			direction = np.dot(normal, - observer_to_point_vector)
			if direction <= 0:
				brightness = 0
			self.brightnesses.append(brightness)

	def __compute_intersections_on_plane(self):
		intersections_on_plane = []
		for point, brightness in zip(self.obj.points, self.brightnesses):
			observer_to_point_vector = np.array(point) - np.array(self.observer)
			distance_to_point = np.linalg.norm(observer_to_point_vector)

			# verify that the point is in the line of sight of the observer
			is_visible_to_observer = True
			step = 0.1
			for m in np.arange(step, distance_to_point - step, step):
				point_m = self.observer + m * observer_to_point_vector
				if self.obj.contains_point(point_m):
					is_visible_to_observer = False

			# only project the points on the camera plane that are visible to the observer
			if is_visible_to_observer:
				intersection_on_plane = self.camera_plane.find_intersection(self.observer, observer_to_point_vector)
				intersections_on_plane.append((intersection_on_plane, distance_to_point, brightness))
		
		return intersections_on_plane

	def show(self):
		self.__compute_illumination()
		intersections_on_plane = self.__compute_intersections_on_plane()

		pixels_on_plane = self.camera_plane.clip_points_to_pixels(intersections_on_plane)

		brightnesses = np.array([[i, brightness] for i, (_, _, brightness) in pixels_on_plane.items()])
		max_brightness = max(brightnesses[:, 1])
		brightnesses = list(map(lambda b: [b[0], b[1] / max_brightness], brightnesses))
		brightnesses = [[i, int(10 * np.around(brightness, decimals=1))] for i, brightness in brightnesses]

		for i, brightness in brightnesses:
			if i % self.camera_plane.nb_pixel_width == 0 and i > 0:
				print("-")
			print(self.brightness_chars[min(brightness, 9)], end='')
		print()


if __name__ == "__main__":
	R = 1
	r = 0.2

	#obj = Torus(R, r)
	obj = Sphere(R)
	obj = Line()

	observer = np.array([2 * R, 0, 0])
	light_source = observer
	
	# observer = np.array([0, 0, 6 * R])
	# light_source = observer
	
	normal = np.array([-1, 0, 0])
	up = np.array([0, 0, 1])
	p0 = Plane.compute_p0(observer, normal)
	camera_plane = Plane(normal, up, p0)
	scene = Scene(obj, light_source, observer, camera_plane)

	scene.show()

	



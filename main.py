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

	def __init__(self, p0, normal, up, horizontal, height, width, nb_pixel_height, nb_pixel_width, pixel_incr):
		self.p0 = p0
		self.normal = normal
		self.up = up
		self.horizontal = horizontal
		self.height = height
		self.width = width
		self.nb_pixel_height = nb_pixel_height
		self.nb_pixel_width = nb_pixel_width
		self.pixel_incr = pixel_incr

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

class Camera:
	def __init__(self, observer, point_to_fix=np.array([0, 0, 0]), horizontal_rotation=0, camera_to_plane_distance=1, aspect_ratio=32/9, height=0.5, nb_pixel_height=64):
		self.camera_point = observer
		self.height = height
		self.width = self.height * aspect_ratio
		self.nb_pixel_height = nb_pixel_height
		self.nb_pixel_width = math.ceil(self.nb_pixel_height * aspect_ratio)
		# TODO split into height_incr and width_incr, because characters displayed on terminal aren't squares, which means a circle isn't round unless we take into account the height/width ratio of a character bounding box
		self.pixel_incr = self.width / self.nb_pixel_width
		
		# compute plane
		normal = normalize_vector(point_to_fix - self.camera_point)
		p0 = self.camera_point + camera_to_plane_distance * normal
		up, horizontal = self.__compute_camera_plane(normal, horizontal_rotation)
		self.plane = Plane(p0, normal, up, horizontal, self.height, self.width, self.nb_pixel_height, self.nb_pixel_width, self.pixel_incr)

	def __compute_camera_plane(self, normal, horizontal_rotation):
		'''
			Compute the 'up' and 'horizontal' vectors.
			When positioned at the camera point and looking towards the point to fix, the 'up' vector is up and the 'horizontal' vector is horizontally to the right.
		'''

		# compute 'up' and 'horizontal' vectors assuming no rotation
		if normal[1] == 0:
			normal_xy_sign = np.sign(normal[0])
			horizontal_vector = normalize_vector(np.array([0, - normal_xy_sign, 0]))
		else:
			frac = - normal[0] / normal[1]
			normal_xy_sign = - np.sign(normal[0]) * np.sign(normal[1])
			horizontal_vector = normal_xy_sign * normalize_vector(np.array([1, frac, 0]))			
		up_vector = normalize_vector(np.cross(horizontal_vector, normal))

		# rotate both 'up' and 'horizontal' vectors
		up_vector_factor = math.cos(horizontal_rotation)
		up_vector_norm = np.linalg.norm(up_vector)
		horizontal_vector_norm = np.linalg.norm(horizontal_vector)
		horizontal_vector_factor = math.sin(horizontal_rotation) * (up_vector_norm / horizontal_vector_norm)

		rotated_up_vector = up_vector_factor * up_vector + horizontal_vector_factor * horizontal_vector
		rotated_horizontal_vector = np.cross(normal, rotated_up_vector)

		return normalize_vector(rotated_up_vector), normalize_vector(rotated_horizontal_vector)

class Scene:
	def __init__(self, obj, light_source, observer, camera, brightness_chars=" :?X#M&%@$"):
		# TODO add possiblity for multiple objects
		self.obj = obj
		self.light_source = light_source
		self.observer = observer
		self.camera = camera
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
				intersection_on_plane = self.camera.plane.find_intersection(self.observer, observer_to_point_vector)
				intersections_on_plane.append((intersection_on_plane, distance_to_point, brightness))
		
		return intersections_on_plane

	def show(self):
		self.__compute_illumination()
		intersections_on_plane = self.__compute_intersections_on_plane()

		pixels_on_plane = self.camera.plane.clip_points_to_pixels(intersections_on_plane)

		brightnesses = np.array([[i, brightness] for i, (_, _, brightness) in pixels_on_plane.items()])
		max_brightness = max(brightnesses[:, 1])
		brightnesses = list(map(lambda b: [b[0], b[1] / max_brightness], brightnesses))
		brightnesses = [[i, int(10 * np.around(brightness, decimals=1))] for i, brightness in brightnesses]

		for i, brightness in brightnesses:
			if i % self.camera.plane.nb_pixel_width == 0 and i > 0:
				print("-")
			print(self.brightness_chars[min(brightness, 9)], end='')
		print()


if __name__ == "__main__":
	R = 1
	r = 0.2

	#obj = Torus(R, r)
	obj = Sphere(R)
	#obj = Line()

	observer = np.array([2 * R, 0, 0])
	light_source = observer
	camera = Camera(observer)
	scene = Scene(obj, light_source, observer, camera)

	scene.show()

	



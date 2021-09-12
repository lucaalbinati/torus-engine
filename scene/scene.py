import numpy as np
from utils import normalize_vector

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
	



import numpy as np
from utils import normalize_vector

class Scene:
	def __init__(self, obj, light_source, observer, camera, ambient_light=1, brightness_chars=" :?X#M&%@$"):
		# TODO add possiblity for multiple objects
		self.obj = obj
		self.light_source = light_source
		self.observer = observer
		self.camera = camera
		self.ambient_light = ambient_light
		self.brightness_chars = brightness_chars

	def __compute_illumination(self):
		self.brightnesses = []
		self.directions = []
		for point, normal in zip(self.obj.points, self.obj.normals):
			observer_to_point_vector = np.array(point) - np.array(self.observer)
			point_to_light_vector = np.array(self.light_source) - np.array(point)
			
			light_direction = np.dot(normal, self.light_source)
			if light_direction > 0:
				# FIXME the farther the light source the weaker the light
				brightness = np.dot(normalize_vector(observer_to_point_vector), normalize_vector(point_to_light_vector)) + self.ambient_light
			else:
				brightness = self.ambient_light

			self.brightnesses.append(brightness)
			direction = np.dot(normal, - observer_to_point_vector)
			self.directions.append(direction)

	def __compute_intersections_on_plane(self):
		intersections_on_plane = []

		for point, brightness, direction in zip(self.obj.points, self.brightnesses, self.directions):
			point_to_observer_vector = np.array(self.observer) - np.array(point)
			distance_to_point = np.linalg.norm(point_to_observer_vector)

			# verify that the point is in the line of sight of the observer
			is_visible_to_observer = True
			step = 0.1
			for m in np.arange(step, distance_to_point - step, step):
				point_m = point + m * point_to_observer_vector
				if self.obj.contains_point(point_m):
					is_visible_to_observer = False
					break

			# only project the points on the camera plane that are visible to the observer
			if is_visible_to_observer and brightness > 0 and direction > 0:
				intersection_on_plane = self.camera.plane.find_intersection(self.observer, point_to_observer_vector)
				intersections_on_plane.append((intersection_on_plane, distance_to_point, brightness))
		
		return intersections_on_plane

	def show(self):
		self.__compute_illumination()
		intersections_on_plane = self.__compute_intersections_on_plane()

		pixels_on_plane = self.camera.plane.clip_points_to_pixels(intersections_on_plane)

		brightnesses = np.array([[i, brightness] for i, (_, _, brightness) in pixels_on_plane.items()])
		max_brightness = max(brightnesses[:, 1])
		# FIXME use absolute light values instead of remapping every time (otherwise not consistant as we move the light source away from the object)
		brightnesses = list(map(lambda b: [b[0], b[1] / max_brightness], brightnesses))

		for i, brightness in brightnesses:
			brightness = 10 * np.around(brightness, decimals=1)
			if 0 < brightness and brightness < 1:
				brightness = 1
			else:
				brightness = int(brightness)

			if i % self.camera.plane.nb_pixel_width == 0 and i > 0:
				print("-")
			print(self.brightness_chars[min(brightness, 9)], end='')
		print()
	



import numpy as np
from utils import normalize_vector

class Scene:
	def __init__(self, obj, light_source, observer, camera, brightness_chars=" .?X#M&%@$"):
		# TODO add possiblity for multiple objects
		self.obj = obj
		self.light_source = light_source
		self.observer = observer
		self.camera = camera
		self.brightness_chars = brightness_chars

	def __compute_illumination(self):
		self.brightnesses = []
		for point, normal in zip(self.obj.points, self.obj.normals):
			brightness = self.light_source.compute_brightness_on_point(self.observer, point, normal)
			self.brightnesses.append(brightness)

	def __compute_intersections_on_plane(self):
		intersections_on_plane = []

		for point, brightness in zip(self.obj.points, self.brightnesses):
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
			if is_visible_to_observer and brightness > 0:
				intersection_on_plane = self.camera.plane.find_intersection(self.observer, point_to_observer_vector)
				intersections_on_plane.append((intersection_on_plane, distance_to_point, brightness))
		
		return intersections_on_plane

	def show(self):
		self.__compute_illumination()
		intersections_on_plane = self.__compute_intersections_on_plane()

		pixels_on_plane = self.camera.plane.clip_points_to_pixels(intersections_on_plane)

		brightnesses = np.array([[i, brightness] for i, (_, _, brightness) in pixels_on_plane.items()])
		# FIXME use absolute light values instead of remapping every time (otherwise not consistant as we move the light source away from the object)

		for i, brightness in brightnesses:
			if brightness == self.light_source.ambient_light:
				brightness_char = self.brightness_chars[0]
			else:
				brightness = brightness / 10
				if 0 < brightness and brightness < 1:
					brightness = 1
				else:
					brightness = int(brightness)
				brightness_char = self.brightness_chars[min(brightness, 9)]

			if i % self.camera.plane.nb_pixel_width == 0 and i > 0:
				print("-")
			print(brightness_char, end='')
		print()
	



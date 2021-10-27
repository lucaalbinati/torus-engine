import numpy as np

class Light:
	def __init__(self, position, intensity=100, ambient_light=1):
		self.position = position
		self.intensity = intensity
		self.ambient_light = ambient_light

	def compute_brightness_on_point(self, observer, point_position, point_normal):
		point_to_observer_vector = observer - point_position
		point_to_observer_factor = np.dot(point_to_observer_vector, point_normal)
		is_visible_to_the_observer = point_to_observer_factor > 0

		if is_visible_to_the_observer:
			point_to_light_vector = self.position - point_position
			point_to_light_factor = np.dot(point_to_light_vector, point_normal)
			is_casting_light_on_point = point_to_light_factor > 0

			if is_casting_light_on_point:
				distance_factor = 1 / np.sum(np.square(point_to_light_vector))
				return self.intensity * distance_factor * point_to_observer_factor * point_to_light_factor + self.ambient_light
			else:
				return self.ambient_light
		else:
			return 0
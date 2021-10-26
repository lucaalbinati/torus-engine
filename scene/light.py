import numpy as np
from utils import normalize_vector

class Light:
	def __init__(self, position, intensity=100, ambient_light=1):
		self.position = position
		self.intensity = intensity
		self.ambient_light = ambient_light

	def compute_brightness_on_point(self, observer, point_position, point_normal):
		point_to_observer_vector = normalize_vector(observer - point_position)
		point_to_light_vector = normalize_vector(self.position - point_position)

		light_to_point_distance = np.linalg.norm(point_to_light_vector)

		point_to_observer_factor = np.dot(point_to_observer_vector, point_normal)
		point_to_light_factor = np.dot(point_to_light_vector, point_normal)

		is_visible_to_the_observer = point_to_observer_factor > 0
		is_casting_light_on_point = point_to_light_factor > 0

		if is_visible_to_the_observer and is_casting_light_on_point:
			distance_factor = 1 / (light_to_point_distance**2)
			return self.intensity * distance_factor * point_to_observer_factor * point_to_light_factor + self.ambient_light
		elif is_visible_to_the_observer:
			return self.ambient_light
		else:
			return 0

	def compute_brightness_on_point2(self, observer, points, normals):
		points_to_observer = np.apply_along_axis(normalize_vector, 1, observer - points)
		points_to_light = np.apply_along_axis(normalize_vector, 1, self.position - points)

		def compute_distance(point_to_light_vector):
			if (point_to_light_vector == np.array([0, 0, 0])).all():
				return 0
			else:
				return 1 / np.sum(np.square(point_to_light_vector))
		light_to_points_distance_factors = np.apply_along_axis(compute_distance, 1, points_to_light)

		points_to_observer_factors = np.einsum('ij,ij->i', points_to_observer, normals)
		points_to_light_factors = np.einsum('ij,ij->i', points_to_light, normals)

		are_visible_to_the_observer = points_to_observer_factors > 0
		are_casting_light = points_to_light_factors > 0

		bools = np.transpose([are_visible_to_the_observer, are_casting_light])

		# brightnesses = np.empty(shape=(len(points),))
		# tt_index = np.argwhere(bools == [True, True])
		# brightnesses[tt_index] = self.intensity * light_to_points_distance_factors[tt_index] * points_to_light_factors[tt_index] + self.ambient_light
		# brightnesses[np.argwhere(bools == [True, False])] = self.ambient_light
		# brightnesses[np.argwhere(bools == [False, True])] = 0
		# brightnesses[np.argwhere(bools == [False, False])] = 0

		def compute_brightness(is_visible_bool, is_casting_light_bool, idx):
			if is_visible_bool and is_casting_light_bool:
				return self.intensity * light_to_points_distance_factors[idx] * points_to_observer[idx] * points_to_light_factors[idx] + self.ambient_light
			elif is_visible_bool:
				return self.ambient_light
			else:
				return 0

		brightnesses = np.empty(shape=(len(points)))
		#brightnesses = np.array([compute_brightness(is_visible_bool, is_casting_light_bool, i) for i, (is_visible_bool, is_casting_light_bool) in enumerate(bools)], dtype=object)
		# print(brightnesses)
		#print(brightnesses.shape)

		# print(brightnesses)
		# print(brightnesses.shape)

		return brightnesses
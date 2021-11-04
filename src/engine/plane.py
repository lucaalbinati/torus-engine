import sys
import numpy as np
from engine.utils import normalize_vector

class Plane:
	def __init__(self, p0, normal, up, horizontal, height, width, nb_pixel_height, nb_pixel_width, pixel_incr_height, pixel_incr_width):
		self.p0 = p0
		self.normal = normal
		self.up = up
		self.horizontal = horizontal
		self.height = height
		self.width = width
		self.nb_pixel_height = nb_pixel_height
		self.nb_pixel_width = nb_pixel_width
		self.pixel_incr_height = pixel_incr_height
		self.pixel_incr_width = pixel_incr_width
		self.top_left_corner = self.__compute_top_left_corner()
		self.init_pixels = self.__compute_init_pixels()

	def __compute_top_left_corner(self):
		return self.p0 - (self.width / 2) * self.horizontal + (self.height / 2) * self.up

	def __compute_init_pixels(self):
		pixels = {}
		for h in range(self.nb_pixel_height):
			h_incr = - self.pixel_incr_height * h
			for w in range(self.nb_pixel_width):
				w_incr = self.pixel_incr_width * w

				point = self.top_left_corner + w_incr * self.horizontal + h_incr * self.up

				i = h * self.nb_pixel_width + w
				pixels[i] = (point, sys.maxsize, 0)
		return pixels

	def get_fresh_init_pixels(self):
		return dict(self.init_pixels)

	def find_intersection(self, vector_start, vector):
		l0 = vector_start
		l = vector

		# d = [(p0-l0) * n] / [n * l]
		p0l0 = self.p0 - l0
		top = np.dot(p0l0, self.normal)
		bottom = np.dot(self.normal, l)
		d = top / bottom

		# intersection point
		p = l0 + l * d
		return p

	def clip_point_to_pixel(self, intersection_on_plane):	
		topleftcorner_to_intersection_point = intersection_on_plane - self.top_left_corner
		horizontal_shift = np.dot(self.horizontal, topleftcorner_to_intersection_point)
		vertical_shift = np.dot(self.up, topleftcorner_to_intersection_point)
		grid_position_w = int(horizontal_shift / self.pixel_incr_width)
		grid_position_h = int(- vertical_shift / self.pixel_incr_height)
		grid_position = grid_position_h * self.nb_pixel_width + grid_position_w
		if grid_position < 0 or grid_position >= len(self.init_pixels):
			return None
		return grid_position
import sys
import numpy as np
from utils import normalize_vector

class Plane:
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

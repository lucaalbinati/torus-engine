import os
import math
import numpy as np
from torusengine.utils import normalize_vector
from torusengine.plane import Plane

class Camera:
	def __init__(self, camera_position, point_to_fix=np.array([0, 0, 0]), horizontal_rotation=0, camera_to_plane_distance=1, nb_pixels=None, character_aspect_ratio=1/2):
		self.camera_point = np.array(camera_position)
		self.point_to_fix = np.array(point_to_fix)
		
		# compute plane vectors
		self.normal = normalize_vector(point_to_fix - self.camera_point)
		p0 = self.camera_point + camera_to_plane_distance * self.normal
		self.up, self.horizontal = self.__compute_camera_plane(self.normal, horizontal_rotation)
		
		# set and compute angular increment constants
		angular_movement_increment = math.pi / 12
		self.cos_increment = math.cos(angular_movement_increment) # cos(⍺)
		self.cos_90_minus_increment = math.cos((math.pi / 2) - angular_movement_increment) # cos((π/2)-⍺)

		# get number of pixels (if running from a terminal window)
		if nb_pixels == None:
			try:
				nb_pixels = os.get_terminal_size()
			except OSError as e:
				nb_pixels = (190, 100)
				print("Not running from a terminal so the number of pixels is set to the default: {}".format(nb_pixels))
		
		# init camera plane
		nb_pixel_width, nb_pixel_height = nb_pixels
		aspect_ratio = nb_pixel_width / (nb_pixel_height / character_aspect_ratio)
		width = 1
		height = width / aspect_ratio
		nb_pixel_height = math.ceil(nb_pixel_width * character_aspect_ratio / aspect_ratio)
		pixel_incr_height = height / nb_pixel_height
		pixel_incr_width = width / nb_pixel_width
		self.plane = Plane(p0, self.normal, self.up, self.horizontal, height, width, nb_pixel_height, nb_pixel_width, pixel_incr_height, pixel_incr_width)

	def __compute_camera_plane(self, normal, horizontal_rotation):
		'''
			Compute the 'up' and 'horizontal' vectors.
			When positioned at the camera point and looking towards the point to fix, the 'up' vector is up and the 'horizontal' vector is horizontally to the right.
		'''

		# compute 'up' and 'horizontal' vectors assuming no rotation
		if normal[0] == 0 and normal[1] == 0:
			horizontal_vector = np.array([0, 1, 0])
		elif normal[0] == 0:
			normal_xy_sign = np.sign(normal[1])
			horizontal_vector = normalize_vector(np.array([normal_xy_sign, 0, 0]))
		elif normal[1] == 0:
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

	def __compute_new_camera_point(self, move):
		rotation_circle_R = np.linalg.norm(self.point_to_fix - self.camera_point)

		if move.is_vertical():
			lateral_direction_vector = self.up * np.sign(move.value)
		elif move.is_horizontal():
			lateral_direction_vector = self.horizontal * np.sign(move.value)

		new_camera_point = rotation_circle_R * (-self.normal * self.cos_increment + lateral_direction_vector * self.cos_90_minus_increment)
		return new_camera_point

	def move(self, move):
		new_camera_point = self.__compute_new_camera_point(move)
		self.__init__(camera_position=new_camera_point)

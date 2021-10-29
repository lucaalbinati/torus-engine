import os
import math
import numpy as np
from utils import normalize_vector
from .plane import Plane

class Camera:
	def __init__(self, observer, point_to_fix=np.array([0, 0, 0]), horizontal_rotation=0, camera_to_plane_distance=1, nb_pixels=os.get_terminal_size(), character_aspect_ratio=1/2):
		self.camera_point = observer
		
		# compute plane vectors
		normal = normalize_vector(point_to_fix - self.camera_point)
		p0 = self.camera_point + camera_to_plane_distance * normal
		up, horizontal = self.__compute_camera_plane(normal, horizontal_rotation)
		
		# init camera plane
		nb_pixel_width, nb_pixel_height = nb_pixels
		aspect_ratio = nb_pixel_width / (nb_pixel_height / character_aspect_ratio)
		width = 1
		height = width / aspect_ratio
		nb_pixel_height = math.ceil(nb_pixel_width * character_aspect_ratio / aspect_ratio)
		pixel_incr_height = height / nb_pixel_height
		pixel_incr_width = width / nb_pixel_width
		self.plane = Plane(p0, normal, up, horizontal, height, width, nb_pixel_height, nb_pixel_width, pixel_incr_height, pixel_incr_width)

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
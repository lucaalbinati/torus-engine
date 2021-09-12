import math
import numpy as np
from utils import normalize_vector
from .plane import Plane

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
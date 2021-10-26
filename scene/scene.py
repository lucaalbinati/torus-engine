import numpy as np
from utils import normalize_vector, get_brightness_char, clear_console

class Scene:
	def __init__(self, obj, light_source, camera):
		# TODO add possiblity for multiple objects
		self.obj = obj
		self.light_source = light_source
		self.camera = camera

	def __compute_illumination(self):
		import time
		begin = time.time()
		self.brightnesses = []
		for point, normal in zip(self.obj.points, self.obj.normals):
			brightness = self.light_source.compute_brightness_on_point(self.camera.camera_point, point, normal)
			self.brightnesses.append(brightness)
		print("old: {}".format(time.time()-begin))
		# self.brightnesses = np.array(list(zip(self.obj.points, self.obj.normals)))
		# self.brightnesses = np.array([self.obj.points, self.obj.normals])
		# np.vectorize(compute_brightness_on_point)(self.obj.points, self.obj.normals)

		# print(self.brightnesses.shape)
		begin = time.time()
		brightnesses2 = self.light_source.compute_brightness_on_point2(self.camera.camera_point, self.obj.points, self.obj.normals)
		print("new: {}".format(time.time()-begin))
		print(self.brightnesses == brightnesses2)
		# print(np.equal(self.brightnesses, brightnesses2).all())
		print(self.brightnesses[4000:4010])
		print(brightnesses2[4000:4010])

	def __compute_pixels(self):
		pixels = self.camera.plane.get_fresh_init_pixels()
		for point, brightness in zip(self.obj.points, self.brightnesses):
			point_to_camera_vector = np.array(self.camera.camera_point) - np.array(point)
			distance_to_point = np.linalg.norm(point_to_camera_vector)

			# only project the points on the camera plane that are visible to the camera
			if brightness > 0:
				intersection_on_plane = self.camera.plane.find_intersection(self.camera.camera_point, point_to_camera_vector)
				pixel = self.camera.plane.clip_point_to_pixel(intersection_on_plane)

				if not pixel in pixels or distance_to_point < pixels[pixel][1]:
					pixels[pixel] = (intersection_on_plane, distance_to_point, brightness)
		
		return pixels

	def __print_pixels(self, pixels):
		clear_console()
		for i, (_, _, brightness) in pixels.items():
			if i % self.camera.plane.nb_pixel_width == 0 and i > 0:
				print("")
			print(get_brightness_char(brightness), end='')
		print()

	def modify_camera(self, camera):
		self.camera = camera

	def modify_light_source(self, light_source):
		self.light_source = light_source

	def show(self):
		self.__compute_illumination()
		pixels = self.__compute_pixels()
		self.__print_pixels(pixels)
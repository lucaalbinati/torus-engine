import time
import numpy as np
from utils import normalize_vector, get_brightness_char, clear_console

class Scene:
	def __init__(self, obj, light_source, camera, fps=5):
		# TODO add possiblity for multiple objects
		self.obj = obj
		self.light_source = light_source
		self.camera = camera
		if not (type(fps) == int and fps >= 1):
			raise Exception("FPS value must be an int greater or equal to 1, instead got '{}'".format(fps))
		self.fps = fps

	def __compute_illumination(self):
		self.brightnesses = [self.light_source.compute_brightness_on_point(self.camera.camera_point, point, normal) for point, normal in zip(self.obj.points, self.obj.normals)]

	def __compute_pixels(self):
		pixels = self.camera.plane.get_fresh_init_pixels()

		# only project the points on the camera plane that are visible to the camera, so we filter out the points with negative brightness
		points_with_positive_brightness = filter(lambda x: x[1] > 0, zip(self.obj.points, self.brightnesses))

		for point, brightness in points_with_positive_brightness:
			point_to_camera_vector = self.camera.camera_point - point
			distance_to_point = np.linalg.norm(point_to_camera_vector)

			intersection_on_plane = self.camera.plane.find_intersection(self.camera.camera_point, point_to_camera_vector)
			pixel = self.camera.plane.clip_point_to_pixel(intersection_on_plane)

			if distance_to_point < pixels[pixel][1]:
				pixels[pixel] = (intersection_on_plane, distance_to_point, brightness)
		
		return pixels

	def __print_pixels(self, pixels):
		clear_console()
		text_to_print = ""
		for i, (_, _, brightness) in pixels.items():
			if i % self.camera.plane.nb_pixel_width == 0 and i > 0:
				text_to_print += "\n"
			text_to_print += get_brightness_char(brightness)
		print(text_to_print)

	def __update_scene(self):
		self.__compute_illumination()
		pixels = self.__compute_pixels()
		self.__print_pixels(pixels)

	def modify_camera(self, camera):
		self.camera = camera

	def modify_light_source(self, light_source):
		self.light_source = light_source

	def start(self, static=False):
		if static:
			self.__update_scene()
		else:
			self.run = True
			while self.run:
				before_comp_time = time.time()

				self.__update_scene()

				computation_time = time.time() - before_comp_time
				sleep_time = (1 / self.fps) - computation_time
				time.sleep(max(sleep_time, 0))

	def move_camera_up(self):
		self.camera.move_up()
	
	def move_camera_down(self):
		self.camera.move_down()

	def move_camera_left(self):
		self.camera.move_left()
	
	def move_camera_right(self):
		self.camera.move_right()
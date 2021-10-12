import time
import numpy as np
from utils import normalize_vector
from scene.camera import Camera
from scene.light import Light

class Animation:

	# TODO generalize to animating camera and object

	def __init__(self, scene, start_point, end_point, FPS=5, animation_duration_in_sec=2):
		self.scene = scene
		self.start_point = start_point
		self.FPS = FPS

		self.nb_frames = FPS * animation_duration_in_sec
		vector_incr_direction = normalize_vector(end_point - start_point)
		vector_norm = np.linalg.norm(end_point - start_point)
		self.vector_incr = vector_incr_direction * (vector_norm / self.nb_frames)

	def animate_camera(self):
		def modify_camera(new_point):
			self.scene.modify_camera(Camera(new_point))
		self.__animate(modify_camera)

	def animate_light(self):
		def modify_light_source(new_point):
			self.scene.modify_light_source(Light(new_point))
		self.__animate(modify_light_source)

	def __animate(self, scene_modification_func):
		excessive_computation_count = 0
		excessive_computations = []

		for i in range(0, self.nb_frames + 1):
			before_comp_time = time.time()

			point = self.start_point + self.vector_incr * i
			scene_modification_func(point)
			self.scene.show()

			after_comp_time = time.time()

			comp_time = after_comp_time - before_comp_time
			sleep_time = (1 / self.FPS) - comp_time

			if sleep_time < 0:
				excessive_computation_count += 1
				excessive_computations.append(comp_time)
				if excessive_computation_count >= 3:
					print("WARNING: computation regularly takes more time than {}s (1/FPS) (takes an average of {:.3f}s)".format(1 / self.FPS, np.mean(excessive_computations)))

			time.sleep(max(sleep_time, 0))

	@staticmethod
	def middle_to_up_camera_animation(scene):
		start_point = np.array([7, 0, 3])
		end_point = np.array([7, 0, 4])
		return Animation(scene, start_point, end_point)

	@staticmethod
	def middle_to_right_light_animation(scene):
		start_point = np.array([3, 0, 0])
		end_point = np.array([0, 3, 4])
		return Animation(scene, start_point, end_point)

	@staticmethod
	def left_to_right_light_animation(scene):
		start_point = np.array([2, -5, 0])
		end_point = np.array([2, 5, 0])
		return Animation(scene, start_point, end_point, animation_duration_in_sec=5)

	@staticmethod
	def down_to_up_light_animation(scene):
		start_point = np.array([3, 0, - 2])
		end_point = np.array([3, 0, 2])
		return Animation(scene, start_point, end_point)
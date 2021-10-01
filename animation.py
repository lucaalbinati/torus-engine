import time
import numpy as np
from utils import normalize_vector
from scene.light import Light

class Animation:

	def __init__(self, scene, light_source_start_point, light_source_end_point, FPS=5, animation_duration_in_sec=2):
		self.scene = scene
		self.light_source_start_point = light_source_start_point
		self.FPS = FPS

		self.nb_frames = FPS * animation_duration_in_sec
		vector_incr_direction = normalize_vector(light_source_end_point - light_source_start_point)
		vector_norm = np.linalg.norm(light_source_end_point - light_source_start_point)
		self.vector_incr = vector_incr_direction * (vector_norm / self.nb_frames)

	def animate(self):
		excessive_computation_count = 0

		for i in range(0, self.nb_frames + 1):
			before_comp_time = time.time()

			point = self.light_source_start_point + self.vector_incr * i
			self.scene.modify_light_source(Light(point))
			self.scene.show()

			after_comp_time = time.time()

			comp_time = after_comp_time - before_comp_time
			sleep_time = (1 / self.FPS) - comp_time

			if sleep_time < 0:
				excessive_computation_count += 1
				if excessive_computation_count >= 3:
					print("WARNING: computation regularly takes more time than {} (1/FPS)".format(1 / self.FPS))

			time.sleep(max(sleep_time, 0))
import numpy as np
from objects.line import Line
from objects.sphere import Sphere
from objects.torus import Torus
from scene.scene import Scene
from scene.camera import Camera
from scene.light import Light
from animation import Animation

if __name__ == "__main__":
	R = 1
	r = 0.2

	#obj = Torus(R, r)
	obj = Sphere(R)
	#obj = Line()

	observer = np.array([7 * R, 0, 0])
	light_source = Light(np.array([10 * R, 0, 0]))
	camera = Camera(observer)
	scene = Scene(obj, light_source, observer, camera)

	light_source_start_point = np.array([3 * R, 0, 0])
	light_source_end_point = np.array([0, 3 * R, 4 * R])
	light_animation = Animation(scene, light_source_start_point, light_source_end_point)

	light_animation.animate()

	#import cProfile
	#cProfile.run('light_animation.animate()')
	
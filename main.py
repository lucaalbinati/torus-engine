import numpy as np
from objects.line import Line
from objects.sphere import Sphere
from objects.torus import Torus
from scene.scene import Scene
from scene.camera import Camera
from scene.light import Light
from animation import Animation
from rotation import Rotation

if __name__ == "__main__":
	obj = Torus()

	observer = np.array([7, 0, 3])
	light_source = Light(np.array([10, 0, 0]))
	camera = Camera(observer)
	scene = Scene(obj, light_source, camera)
	# scene.show()

	# light_animation = Animation.middle_to_right_light_animation(scene)
	# light_animation.animate_light()

	# rotation_animation = Rotation.cool_around_yz(scene)
	# rotation_animation.animate()

	import cProfile
	cProfile.run('scene.show()')
import sys
import math
import numpy as np
from utils import normalize_vector
from objects.line import Line
from objects.sphere import Sphere
from objects.torus import Torus
from scene.scene import Scene
from scene.camera import Camera
from scene.plane import Plane

if __name__ == "__main__":
	R = 1
	r = 0.2

	#obj = Torus(R, r)
	obj = Sphere(R)
	#obj = Line()

	observer = np.array([2 * R, 0, 0])
	light_source = observer
	camera = Camera(observer)
	scene = Scene(obj, light_source, observer, camera)

	scene.show()

	



import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, "{}/..".format(dir_path))

import numpy as np
from objects.torus import Torus
from scene.scene import Scene
from scene.light import Light
from scene.camera import Camera

obj = Torus()

observer = np.array([7, 0, 3])
light_source = Light(np.array([10, 0, 0]))
camera = Camera(observer)
scene = Scene(obj, light_source, camera)

import cProfile
#cProfile.run('scene._Scene__compute_illumination()')
scene._Scene__compute_illumination()
#print(scene.brightnesses)
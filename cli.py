import sys
import numpy as np
from threading import Thread
from pynput import keyboard
from utils import list_of_all_objects
from scene.scene import Scene
from scene.camera import Camera
from scene.light import Light
from animation import Animation
from rotation import Rotation

command_line_options = {
	"-h": "help",
	"-o": "objects (default is Torus)",
	"-l": "light source position, as a 3 tuple: x y z (default is '10 0 0')",
	"-c": "camera position, as a 3 tuple: x y z (default is '7 0 3')"
}

all_objects_class_name = list_of_all_objects()
DEFAULT_OBJ = "torus"

def print_help():
	print("The program takes these as arguments:\n")
	for command_line_option, description in command_line_options.items():
		print("  {}\t{}".format(command_line_option, description))
	print()

def import_and_get_object_class(obj_name):
	module = __import__("objects.{}".format(obj_name.lower()), fromlist=[obj_name.capitalize()])
	class_ = getattr(module, obj_name.capitalize())
	return class_

def parse_position_tuple(command_line_option, position_description):
	x_idx = sys.argv.index(command_line_option) + 1
	y_idx = sys.argv.index(command_line_option) + 2
	z_idx = sys.argv.index(command_line_option) + 3
	if z_idx >= len(sys.argv):
		raise Exception("Expecting the following after the command line option '{}':\n  x y z\twhere x, y and z are integers or floats".format(command_line_option))

	x = sys.argv[x_idx]
	y = sys.argv[y_idx]
	z = sys.argv[z_idx]

	try:
		return np.array([float(x), float(y), float(z)])
	except ValueError as e:
		raise Exception("The values for the {} position must be integers or floats".format(position_description))

def on_press(key):
	if key == keyboard.Key.up:
		scene.move_camera_up()
	elif key == keyboard.Key.down:
		scene.move_camera_down()
	elif key == keyboard.Key.left:
		scene.move_camera_left()
	elif key == keyboard.Key.right:
		scene.move_camera_right()
	elif key == keyboard.KeyCode.from_char('o'):
		curr_obj_class_name = type(scene.obj).__name__.lower()
		curr_index = all_objects_class_name.index(curr_obj_class_name)
		next_index = (curr_index + 1) % len(all_objects_class_name)
		new_obj = import_and_get_object_class(all_objects_class_name[next_index])()
		scene.change_obj(new_obj)
	elif key == keyboard.KeyCode.from_char('.'):
		scene.increment_light_source_intensity()
	elif key == keyboard.KeyCode.from_char(','):
		scene.decrement_light_source_intensity()
	elif key == keyboard.Key.esc or key == keyboard.KeyCode.from_char('\x03'):
		scene.run = False
		return False

if __name__ == "__main__":

	if "-h" in sys.argv:
		print_help()
		exit(0)

	# Parse object
	if "-o" in sys.argv:
		obj_idx = sys.argv.index("-o") + 1
		if obj_idx >= len(sys.argv):
			raise Exception("Expecting something after the command line option '-o'")

		obj_class_name = sys.argv[obj_idx].lower()
		if not obj_class_name in all_objects_class_name:
			raise Exception("The value after '-o' should be either: {}".format(", ".join(all_objects_class_name)))
		
		class_ = import_and_get_object_class(obj_class_name)
	else:
		class_ = import_and_get_object_class(DEFAULT_OBJ)
	obj = class_()

	# Parse light source position
	if "-l" in sys.argv:
		light_source_position = parse_position_tuple("-l", "light source")
	else:
		light_source_position = np.array([10, 0, 0])
	light_source = Light(light_source_position)
	
	# Parse camera position
	if "-c" in sys.argv:
		camera_position = parse_position_tuple("-c", "camera")
	else:
		camera_position = np.array([7, 0, 3])
	camera = Camera(camera_position)

	# Should the scene update only once (static) or continously?
	static = "--static" in sys.argv

	# Init scene
	scene = Scene(obj, light_source, camera)

	# Start scene in new thread
	thread = Thread(target=scene.start, args=[static])
	thread.start()
	
	# Listen to keyboard inputs
	if not static:
		with keyboard.Listener(on_press=on_press) as listener:
			listener.join()

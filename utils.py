import sys
import numpy as np

brightness_char_zero = " "
brightness_chars_dict = {
	(0, 1): ".",
	(1, 7): "?",
	(7, 14): "X",
	(14, 20): "#",
	(20, 26): "M",
	(26, 32): "&",
	(32, 37): "%",
	(37, 42): "@",
	(42, sys.maxsize): "$"
}

def get_brightness_char(brightness):
	if brightness == 0:
		return brightness_char_zero
	else:
		for (lower, upper), char in brightness_chars_dict.items():
			if lower <= brightness and brightness < upper:
				return char

def normalize_vector(vector):
		vector = np.array(vector)
		norm = np.linalg.norm(vector)
		if norm == 0:
			return vector
		else:
			return vector / norm
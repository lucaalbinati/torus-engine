from enum import Enum

class Move(Enum):
	UP = 1
	DOWN = -1
	LEFT = -2
	RIGHT = 2

	def is_vertical(self):
		return self == Move.UP or self == Move.DOWN

	def is_horizontal(self):
		return self == Move.LEFT or self == Move.RIGHT
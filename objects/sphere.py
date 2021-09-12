import math
import numpy as np
from utils import normalize_vector

class Sphere:
	def __init__(self, R, theta_step=100, phi_step=100):
		self.R = R
		self.theta_step = theta_step
		self.phi_step = phi_step
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / self.theta_step)
		self.phis = np.arange(0, math.pi, math.pi / self.phi_step)
		self.points = [self.point_equation(theta, phi) for theta in self.thetas for phi in self.phis]
		self.normals = [self.normal_equation(theta, phi) for theta in self.thetas for phi in self.phis]

	def point_equation(self, theta, phi):
		return np.array([
				self.R * math.cos(theta) * math.sin(phi),
				self.R * math.sin(theta) * math.sin(phi),
				self.R * math.cos(phi)
			])

	def normal_equation(self, theta, phi):
		return normalize_vector(np.array([
				math.cos(theta) * math.sin(phi),
				math.sin(theta) * math.sin(phi),
				math.cos(phi)
			]))

	def contains_point(self, point):
		# FIXME why isn't the front of the sphere showing?
		x, y, z = point[0], point[1], point[2]
		return (x**2 + y**2 + z**2) <= self.R
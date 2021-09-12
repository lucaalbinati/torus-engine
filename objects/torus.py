import math
import numpy as np
from utils import normalize_vector

class Torus:
	def __init__(self, R, r, theta_step=100, phi_step=100):
		self.R = R
		self.r = r
		self.theta_step = theta_step
		self.phi_step = phi_step
		self.thetas = np.arange(0, 2 * math.pi, 2 * math.pi / self.theta_step)
		self.phis = np.arange(0, 2 * math.pi, 2 * math.pi / self.phi_step)
		self.points = [self.point_equation(theta, phi) for theta in self.thetas for phi in self.phis]
		self.normals = [self.normal_equation(theta, phi) for theta in self.thetas for phi in self.phis]
		
	def point_equation(self, theta, phi):
		return np.array([
				self.R * math.cos(theta) + r * math.cos(phi),
				self.R * math.sin(theta) + r * math.cos(phi),
				self.r * math.sin(phi)
			])

	def normal_equation(self, theta, phi):
		return normalize_vector(np.array([
				math.cos(phi),
				math.cos(phi),
				math.sin(phi)
			]))

	def contains_point(self, point):
		x, y, z = point[0], point[1], point[2]
		contains = True
		contains = contains and (self.R - self.r <= abs(x) <= self.R + self.r)
		contains = contains and (self.R - self.r <= abs(y) <= self.R + self.r)
		contains = contains and (0 <= abs(z) <= self.r)
		return contains
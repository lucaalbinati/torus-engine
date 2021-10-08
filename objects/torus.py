import math
import numpy as np
from utils import normalize_vector, rotate

class Torus:
	def __init__(self, R=1.0, r=0.2, theta_step=100, phi_step=100):
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
				(self.R + self.r * math.cos(phi)) * math.cos(theta),
				(self.R + self.r * math.cos(phi)) * math.sin(theta),
				self.r * math.sin(phi)
			])

	def normal_equation(self, theta, phi):
		return normalize_vector(np.array([
				math.cos(phi),
				math.cos(phi),
				math.sin(phi)
			]))

	def rotate(self, rotation_matrix_func, theta):
		self.points, self.normals = rotate(rotation_matrix_func, theta, self.points, self.normals)
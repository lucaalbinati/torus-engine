import numpy as np

def normalize_vector(vector):
		vector = np.array(vector)
		norm = np.linalg.norm(vector)
		if norm == 0:
			return vector
		else:
			return vector / norm
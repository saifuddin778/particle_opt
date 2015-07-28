#--a separate object definition for the particle

class Particle(object):
	def __init__(self):
		self.vals = None
		self.p_best = 0.0
		self.velocity = 0.0

	def get_vals(self):
		return self.vals

	def get_val_by_j(self, j):
		return self.vals[j]

	def get_p_best(self):
		return self.p_best

	def get_velocity(self):
		return self.velocity

	def set_pbest(self, p_best):
		self.p_best = p_best

	def set_vals(self, vals):
		self.vals = vals

	def set_velocity(self, velocity):
		self.velocity = velocity

	def get_total(self):
		return sum(self.vals)



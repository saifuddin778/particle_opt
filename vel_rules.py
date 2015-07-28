class vel_rules(object):
	def __init__(self, v_max):
		self.v_max = v_max
		self.rule_map = {
			'standard': self.standard
		}

	def get_rule(self, particle, g_best_particle, g_best_particle_val, rule=False):
		if not rule:
			return self.rule_map['standard'](particle, g_best_particle, g_best_particle_val)
		else:
			return self.rule_map[rule](particle, g_best_particle, g_best_particle_val)

	def standard(self, particle, g_best_particle, g_best_particle_val):
		
import sys, os, math, random
from particle import Particle
from objective_method import objective

particles = []
movement_trace = []
max_particle_val = 0

def init_particles(n_particles, min_, max_, dimensions):
	"""
	Declaring the particles.
	"""
	for _ in range(n_particles):
		new_particle = Particle()
		val_ = random.sample(range(min_, max_), dimensions); p_best = objective(val_);
		new_particle.set_vals(val_)
		new_particle.set_pbest(p_best)
		particles.append(new_particle)


def ang(cent, vals): 
	"""
	#-- cos_inv((a.b)/(|a|*|b|))
	"""
	try:
		angle_ = math.cos(sum(a*b for a,b in zip(cent, vals)) / (mag(vals) *  mag(cent))) 
	except ZeroDivisionError:
		angle_ = 0.0
	return angle_


def mag(vals):
	"""
	magnitude of the particle
	"""
	return math.sqrt(sum(map(lambda p: math.pow(p, 2), vals)))


def init_trace(n_particles):
	"""
	Constructs the tracing log which tracks the movement of particles in 2 dimensions only..
	--We build these dimensions as ("objective(particle)", "-20")
	"""
	for i in range(n_particles):
		vals_ = particles[i].get_vals()
		movement_trace.append({
			'id': i,
			'x': objective(vals_),
			'y': -100,
			'new_x': objective(vals_),
			'new_y': -100
			})


def set_trace(i, old, new):
	"""
	Updates the location trace for the particle
	"""
	movement_trace.append({
		'id': i,
		'x': objective(old),
		'y': -100,
		'new_x': objective(new),
		'new_y': -100
		})


def write_trace(movement_trace, results):
	"""
	Writes movement trace of the particles in a file for visualization
	"""
	main_dir = os.path.dirname(__file__)
	rel_path = "vis/data/pso_data1.js"
	abs_file_path = os.path.join(main_dir, rel_path)
	f = open(abs_file_path, 'wb')
	data = "var data = "+str(movement_trace)+";"+"\n"
	data += "var results = "+str(results)+";"+"\n"
	f.write(data)
	f.close()

class pso():
	def __init__(self, particle_count, dimensions, v_max, max_epochs, min_init, max_init, target, visualize=False):
		self.min_val = min_init #--min val of vector
		self.max_val = max_init #--max val of vector
		self.target = target #--target

		self.max_particles = particle_count #--total particles in the swarm
		self.max_inputs = dimensions #--dimensions of each particle

		self.g_best = 0 #--global best value
		self.g_best_test = 0 #--global best value test
		self.done = False #--indicator if the target is met or iterations done

		self.v_max = v_max #--maximum velocity shift value

		self.epoch = 0 #--iteration at n-th stage
		self.max_epochs = max_epochs #--maximum iterations allowed
		self.objective = objective #--the desired objective function
		self.visualize = visualize #--if the results are to be visualized

		init_particles(self.max_particles, self.min_val, self.max_val, self.max_inputs)
		init_trace(self.max_particles)

	def get_nearest(self):
		"""
		Returns the particle that is nearest to the 
		target in terms of its magnitude
		"""
		min_i = 0
		min_val = self.objective(particles[min_i].get_vals())

		for i in range(self.max_particles):
			if i != min_i:
				if math.fabs(self.target - self.objective(particles[i].get_vals())) < math.fabs(self.target - min_val):
					min_i = i
					min_val = self.objective(particles[min_i].get_vals())
		return min_i

	def set_velocity(self, g_best):
		"""
		Sets the velocity for the particles based on the standard rule defined by Kennedy & Eberhart(1995).
		-- The particle that is farthest from the target, its velocity is changed the most (<= self.v_max)
		-- The particle that is closest to the target (including g_best), its velocity is changed the least.
		"""
		g_best_val = self.objective(particles[g_best].get_vals())

		for i in range(self.max_particles):
			particle_ = particles[i]
			current_val = self.objective(particle_.get_vals())
			
			v_val = particle_.get_velocity() + 2  * random.random() * (
						particle_.get_p_best() - self.objective(particle_.get_vals())
					) + 2 * random.random() * (
						g_best_val - self.objective(particle_.get_vals())
					)

			if v_val > self.v_max:
				particle_.set_velocity(self.v_max)
			elif v_val < -self.v_max:
				particle_.set_velocity(-self.v_max)
			else:
				particle_.set_velocity(v_val)


	def update_particles(self, g_best):
		"""
		Updates the particles values
		"""
		for i in range(self.max_particles):
			update = []
			for j in range(self.max_inputs):
				if particles[i].get_val_by_j(j) != particles[g_best].get_val_by_j(j):
					update.append(
							particles[i].get_val_by_j(j) + math.floor(particles[i].get_velocity())
						)
				else:
					update.append(
							particles[i].get_val_by_j(j)
						)

			#--updating movement trace for the particle
			old_vals = particles[i].get_vals()
			particles[i].set_vals(update)
			new_vals = particles[i].get_vals()
			set_trace(i, old_vals, new_vals)


	def optimize(self):
		"""
		trains/fits the particles to catch the target 
		under the given number of pre-fixed iterations
		"""
		victor = 0
		found = False

		while not self.done:
			if self.epoch < self.max_epochs:
				for i in range(self.max_particles):					
					if self.objective(particles[i].get_vals()) == self.target:
						victor = i
						self.done = True
						found = True
						print "FOUND!", self.objective(particles[i].get_vals()), self.target
						break

				new_best = self.get_nearest()
				a_particle = particles[self.g_best]

				if math.fabs(self.target - self.objective(particles[new_best].get_vals())) < math.fabs(self.target - self.objective(a_particle.get_vals())):
					self.g_best = new_best

				self.set_velocity(self.g_best)
				self.update_particles(self.g_best)
				self.epoch += 1
			else:
				self.done = True
		if found:
			print "particle %d is the victor: %s" % (victor, str(particles[victor].get_vals()))
		else:
			print "exact match not found. %d is the nearest: %s" % (victor, str(particles[victor].get_vals()))
		
		print "epochs: %d  out of %d completed" % (self.epoch, self.max_epochs)

		#--add the achieved
		movement_trace.append({
			'id': -1,
			'x': objective(particles[victor].get_vals()),
			'y': -100,
			'new_x': objective(particles[victor].get_vals()),
			'new_y': -100
		})

		#--add the target
		movement_trace.append({
			'id': -2,
			'x': self.target,
			'y': -100,
			'new_x': self.target,
			'new_y': -100
		})

		results = {'victor': particles[victor].get_vals(), 
				'index': victor, 
				'value': objective(particles[victor].get_vals()), 
				'target_value': self.target,
				'max_epochs': self.epoch,
				'v_max': self.v_max,
				'n_particles': self.max_particles}
		
		#--visualize if demanded..
		if self.visualize:
			write_trace(movement_trace, results)
			print "visual trace created..please check viz/pso_index.html"
		return results

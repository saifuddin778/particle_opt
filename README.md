# particle_opt
An implementation of Particle Swarm Optimization algorithm. 

This implementation is very basic, but do provides an editable objective function (in the `objective_method.py`) file, that can be modified accordingly. It provides a [**Visualizing Feautre**] (http://saif778.pythonanywhere.com/pso/) for animating the performance and activity of particles as they trace and swarm their given target (using `visualize=True` parameter in the main method). 

```python
from particle_opt.pso import pso
p = pso(particle_count=50, 
        dimensions=7, 
        v_max=10, 
        max_epochs=200, 
        min_init=10,
        max_init=150, 
        target=450,
        visualize=True)
result = p.optimize()
```
For instance, based on the defualt objective function of sum, the result can be:
```python
{'index': 32, 'target_value': 450, 'n_particles': 50, 'value': 450.0, 'v_max': 10, 'max_epochs': 6, 'victor': [19.0, 85.0, -4.0, 75.0, 71.0, 83.0, 121.0]}
```
Where:
* `index` is the index of the victor/winning particle.
* `target_value` is the target to be achieved by the particle using objective function.
* `n_particles` is the number of particles employed.
* `value` is the value of the victor/winning particle. (should be equal to target for success)
* `v_max` is the maximum velocity for the swarming particles.
* `max_epochs` is the total epochs allowed.
* `victor` is the values for the winning particle.

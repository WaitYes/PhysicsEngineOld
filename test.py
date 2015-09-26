import numpy
from pprint import pprint
import physics_engine


for i in range(10):
    position = numpy.random.uniform(-1000, 1000, (3,1))
    velocity = numpy.random.uniform(-1, 1, (3,1))
    radius = numpy.random.uniform(1, 5)
    mass = numpy.random.uniform(1, 10)
    new_object = physics_engine.SpaceObject(position, velocity, radius, mass)
#    new_visualization = create_sphere_visual(new_object, color.white, radius)
#    objects_and_visual_pairs.append([new_object, new_visualization])


for i in range(0):
    position = numpy.random.uniform(-10, 10, (3,1))
    velocity = numpy.random.uniform(0, 0, (3,1))
    radius = numpy.random.uniform(5, 10)
    mass = radius*500.
    new_object = physics_engine.SpaceObject(position, velocity, radius, mass, False, True)
#    new_visualization = create_sphere_visual(new_object, color.cyan, radius)
#    objects_and_visual_pairs.append([new_object, new_visualization])

pprint(list(physics_engine.collision_detector_and_resolver.objects_max_and_min))

physics_engine.go_forward_one_time_step()

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

pprint(list(physics_engine.collision_detector_and_resolver.objects_max_and_min))



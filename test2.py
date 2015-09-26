import physics_engine
import numpy

object1 = physics_engine.SpaceObject([[0.], [0.], [0.]], [[0.], [0.], [0.]], 5)

object2 = physics_engine.SpaceObject([[0.], [0.], [0.]], [[1000.], [0.], [0.]], 5)

physics_engine.go_forward_one_time_step()
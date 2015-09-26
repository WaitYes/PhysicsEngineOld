from operator import itemgetter
import numpy


__author__ = 'Jacob'


dt = 1./30.
e = .7


objects_effected_by_collisions = []
objects_NOT_effected_by_collisions = []
gravity_sources = []


class DetectAndResolveAllCollisions:
    def __init__(self):
        # Used for the grid collision detection method. Keeps track of how far along each dimension each object stretches.
        self.objects_max_and_min = ([], [], [])

    def add_object_to_max_and_min_lists(self, object_to_be_updated):
        for dimension_index in range(len(self.objects_max_and_min)):
            dimension = self.objects_max_and_min[dimension_index]
            # The additional .01 is so the collision detector will pick up objects that are just barely touching.
            object_max = object_to_be_updated.position[dimension_index] + object_to_be_updated.radius + .01
            object_min = object_to_be_updated.position[dimension_index] - object_to_be_updated.radius - .01
            dimension.append([object_to_be_updated, object_max])
            dimension.append([object_to_be_updated, object_min])
            dimension.sort(key=itemgetter(1))

    def detect_and_resolve_all_collisions(self):

        def update_all_max_and_min_values(objects_to_be_updated=objects_effected_by_collisions+objects_NOT_effected_by_collisions):
            def update_object_in_dimension(dimension_index, space_object):
                dimension = self.objects_max_and_min[dimension_index]

                inserting = 'max'

                for object_number_pair in dimension:
                    object_to_compare_against = object_number_pair[0]

                    if space_object == object_to_compare_against:
                        if inserting == 'max':
                            # The additional .01 is so the collision detector will pick up objects that are just barely touching.
                            object_number_pair[1] = space_object.position[dimension_index] + space_object.radius + .01
                            inserting = 'min'
                        else:
                            object_number_pair[1] = space_object.position[dimension_index] - space_object.radius - .01
                            break

            for dimension_index in range(len(self.objects_max_and_min)):
                for space_object in objects_to_be_updated:
                    update_object_in_dimension(dimension_index, space_object)

                self.objects_max_and_min[dimension_index].sort(key=itemgetter(1))

        def detect_all_collisions():
            def collision_detection_grid_method():

                def checking_single_dimension(dimension):
                    potentially_colliding_pairs_in_one_dimension = []
                    current_list_of_potentially_colliding_objects = []

                    for object_number_pair in dimension:
                        space_object = object_number_pair[0]

                        if space_object in current_list_of_potentially_colliding_objects:
                            current_list_of_potentially_colliding_objects.remove(space_object)
                            for potentially_colliding_object in current_list_of_potentially_colliding_objects:
                                # To make sure the objects in the pairs are in the same order every time they are listed
                                # as potentially colliding:
                                if space_object > potentially_colliding_object:
                                    potentially_colliding_pairs_in_one_dimension.append([space_object, potentially_colliding_object])
                                else:
                                    potentially_colliding_pairs_in_one_dimension.append([potentially_colliding_object, space_object])
                        else:
                            current_list_of_potentially_colliding_objects.append(space_object)

                    return potentially_colliding_pairs_in_one_dimension

                potentially_colliding_pairs_in_0_dimension = checking_single_dimension(self.objects_max_and_min[0])
                potentially_colliding_pairs_in_1_dimension = checking_single_dimension(self.objects_max_and_min[1])
                potentially_colliding_pairs_in_2_dimension = checking_single_dimension(self.objects_max_and_min[2])

                potentially_colliding_pairs = []

                for potentially_colliding_pair in potentially_colliding_pairs_in_0_dimension:
                    if (potentially_colliding_pair in potentially_colliding_pairs_in_1_dimension and
                            potentially_colliding_pair in potentially_colliding_pairs_in_2_dimension):

                        potentially_colliding_pairs.append(potentially_colliding_pair)

                return potentially_colliding_pairs

            def collision_detection_distance_between_method(potentially_colliding_pairs):

                def distance_intersecting(potentially_colliding_pair):
                    space_object1 = potentially_colliding_pair[0]
                    space_object2 = potentially_colliding_pair[1]
                    distance_pair_intersecting = 0
                    if space_object1.radius != 0 or space_object2.radius != 0:
                        vector_between_centers = space_object1.position - space_object2.position
                        distance_between_centers = numpy.linalg.norm(vector_between_centers)
                        if distance_between_centers <= space_object1.radius + space_object2.radius:
                            distance_pair_intersecting = (space_object1.radius + space_object2.radius) - distance_between_centers

                    return distance_pair_intersecting  # distance_pair_intersecting is negative if no collision

                for potentially_colliding_pair in potentially_colliding_pairs:
                    distance_intersecting(potentially_colliding_pair)

            potentially_colliding_pairs_from_grid_method = collision_detection_grid_method()

            all_colliding_pairs = collision_detection_distance_between_method(potentially_colliding_pairs_from_grid_method)
            return all_colliding_pairs

        def shift_all_intersecting_objects_back(self, objects_to_be_shifted):
            def shift_intersecting_pair_back(space_object1, space_object2):
                pass
                #update_all_max_and_min_values()

            # Loop: after shifting one pair, run collision detection to see if
            # they've been moved into any other objects. If they have, then
            # shift those other objects back, otherwise, move onto the next pair.

        def apply_impulses_to_colliding_objects(self):
            # must handle groups of colliding objects
            def apply_impulse_to_colliding_pair(space_object1, space_object2):
                pass

        update_all_max_and_min_values()
        collisions = True
        while collisions:
            colliding_objects = detect_all_collisions()
            if len(colliding_objects) == 0:
                collisions = False
            else:
                shift_all_intersecting_objects_back(colliding_objects)
        apply_impulses_to_colliding_objects(colliding_objects)


collision_detector_and_resolver = DetectAndResolveAllCollisions()


class SpaceObject:
    def __init__(self, position, velocity, radius=0., mass=1.,
                 effected_by_collisions=True, has_gravitational_pull=False):

        self.position = position
        self.velocity = velocity
        self.sum_of_forces = numpy.array([[0.], [0.], [0.]])
        self.radius = numpy.abs(radius)
        self.mass = mass
        self.effected_by_collision = effected_by_collisions
        self.has_gravitational_pull = has_gravitational_pull

        if effected_by_collisions:
            objects_effected_by_collisions.append(self)
        else:
            objects_NOT_effected_by_collisions.append(self)
        if has_gravitational_pull:
            gravity_sources.append(self)

        collision_detector_and_resolver.add_object_to_max_and_min_lists(self)

    def move(self):
        acceleration = self.sum_of_forces / self.mass
        self.velocity = acceleration * dt + self.velocity
        self.position = self.velocity * dt + self.position
        self.sum_of_forces = numpy.array([[0.], [0.], [0.]])


def calculate_all_gravitational_forces():
    def calculate_gravitational_force():
        pass

    #calculate gravitational force for each pair of gravity source and movable object


def move_all_movable_objects():

    for space_object in (objects_effected_by_collisions + objects_NOT_effected_by_collisions):
        space_object.move()


def go_forward_one_time_step():
    #calculate_all_gravitational_forces()
    move_all_movable_objects()
    collision_detector_and_resolver.detect_and_resolve_all_collisions()
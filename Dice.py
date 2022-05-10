import itertools


class Dice(object):
    def __init__(self, degree):
        self.degree = degree
        self.face_values = {}
        self.corners = []

    def set_face(self, face_id, face_value):
        self.face_values[face_id] = face_value

    def add_corner(self, face_ids: list):
        if len(face_ids) != self.degree:
            raise ValueError("Faces per corner must be equal to the degree of the dice")
        self.corners.append(face_ids)

    def permutations(self):
        for face_ids in self.corners:
            for perm in itertools.permutations(face_ids):
                yield perm

    def get_closest_values(self, values: list):
        closest_face_ids = None
        closest_errors = None
        closest_error_sum = float('inf')
        for face_ids in self.permutations():
            errors = [values[i] - self.face_values[face_ids[i]] for i in range(self.degree)]
            error_sum = sum([abs(e) for e in errors])
            if error_sum < closest_error_sum:
                closest_errors = errors
                closest_face_ids = face_ids
                closest_error_sum = error_sum
        return closest_face_ids, closest_errors

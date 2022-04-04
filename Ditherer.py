from PIL import Image

import Dice


class Ditherer(object):

    def dither(self, dice: Dice, images: list, weights=None):
        if weights is None:
            # Floyd Steinberg weights
            weights = {(1, 0): 7 / 16, (-1, 1): 3 / 16, (0, 1): 5 / 16, (1, 1): 1 / 16}
        if dice.degree < len(images):
            raise ValueError("Can draw up to " + dice.degree + " images with provided dice due to it's degree")
        size = None
        for i in range(len(images)):
            if size is None:
                size = images[i].size
            elif size != images[i].size:
                raise ValueError("Images must be the same size")
        images_pixels = [img.load() for img in images]
        images_errors = [{(x, y): 0 for x in range(size[0]) for y in range(size[1])} for _ in images]
        board = {}
        for x in range(size[0]):
            for y in range(size[1]):
                pixel_values = [images_pixels[i][x, y] + images_errors[i][x, y] for i in range(len(images))]
                face_ids, errors = dice.get_closest_values(pixel_values)
                self.push_errors(x, y, errors, weights, images_errors, size)
                board[x, y] = face_ids
        return board

    def push_errors(self, x, y, errors, weights: dict, images_errors: list, size):
        for image_errors, error in zip(images_errors, errors):
            for offset, weight in weights.items():
                x_curr = x + offset[0]
                y_curr = y + offset[1]
                if size[0] > x_curr > -1 and size[1] > y_curr > -1:
                    image_errors[x + offset[0], y + offset[1]] += error * weight

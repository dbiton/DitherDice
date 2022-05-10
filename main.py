from Ditherer import Ditherer
from Dice import Dice
from PIL import Image


def main():
    dice = Dice(3)

    dice.set_face(1, 0)
    dice.set_face(2, 1*255/5)
    dice.set_face(3, 2*255/5)
    dice.set_face(4, 3*255/5)
    dice.set_face(5, 4*255/5)
    dice.set_face(6, 255)

    dice.add_corner([1, 2, 3])
    dice.add_corner([1, 2, 4])
    dice.add_corner([1, 4, 5])
    dice.add_corner([1, 3, 4])
    dice.add_corner([2, 3, 6])
    dice.add_corner([2, 4, 6])
    dice.add_corner([3, 5, 6])
    dice.add_corner([4, 5, 6])

    images = [Image.open('1.jpg').convert("L"), Image.open('2.jpg').convert("L"), Image.open('3.jpg').convert("L")]
    ditherer = Ditherer()
    board = ditherer.dither(dice, images)

    file_dice = open('dice_pos.txt', 'w')
    width, height = images[0].size
    file_dice.write(str(width)+'\n'+str(height)+'\n')
    for face_id in board.values():
        file_dice.write(str(face_id)+'\n')

    images_dithered = [Image.new(mode="L", size=image.size) for image in images]
    for index, values in board.items():
        for value, image_dithered in zip(values, images_dithered):
            image_dithered.putpixel(index, int(value * 255 / 6))
    for i, image in enumerate(images_dithered):
        image.save("dither" + str(i) + ".jpg")


if __name__ == "__main__":
    main()

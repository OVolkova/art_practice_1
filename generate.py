import random as rd
import numpy as np
import cv2


COLORS = [
          (255, 255, 255),  # white
          (0, 0, 205),  # blue
          (75, 0, 130),  # purple
          (0, 128, 0),  # green
          (255, 255, 51),  # yellow
          (255, 25, 25),  # red
          (0, 0, 0),  # black
          (255, 165, 0),  # orange
          ]
GRAY = (192,192,192)
N_OF_BLOCKS = 6


def set_channel(i, array, row, col, b, colors, gray):
    """
    Fill sample from start row and col, fill channel i with colors.
    :param i: number of channel to fill in
    :param array: squared picture as np.array in format(RGB channels, size, size)
    :param row: start row index of sample
    :param col: start col index of sample
    :param b: block size - each sample is divided on 6 blocks
    :param colors: shuffled colors
    :param gray: gray color
    :return: squared picture as np.array in format(RGB channels, size, size) with filled sampled channel i
    """
    # gray
    array[i, (row+2*b):(row+4*b), (col+2*b):(col+4*b)] = gray[i]

    # 0: upper left outer
    array[i, (row+0*b):(row+1*b),  col:(col + 3*b)] = colors[0][i]
    array[i, (row+1*b):(row+2*b),  col:(col+b)] = colors[0][i]

    # 1: upper left inner
    array[i, (row+1*b):(row+2*b),  (col+b):(col + 3*b)] = colors[1][i]
    array[i, (row+2*b):(row+3*b),  col:(col + 2*b)] = colors[1][i]

    # 2: upper right outer
    array[i, (row+0*b):(row+1*b), (col + 3*b):(col + 6*b)] = colors[2][i]
    array[i, (row+1*b):(row+2*b),  (col + 5 * b):(col+6*b)] = colors[2][i]

    # 3: upper right inner
    array[i, (row+1*b):(row+2*b), (col + 3*b):(col + 5*b)] = colors[3][i]
    array[i, (row+2*b):(row+3*b), (col + 4*b):(col + 6*b)] = colors[3][i]

    # 4: lower left outer
    array[i, (row+5*b):(row+6*b), col:(col + 3 * b)] = colors[4][i]
    array[i, (row+4*b):(row+5*b), col:(col+b)] = colors[4][i]

    # 5: lower left inner
    array[i, (row+4*b):(row+5*b), (col + b):(col + 3 * b)] = colors[5][i]
    array[i, (row+3*b):(row+4*b), col:(col + 2 * b)] = colors[5][i]

    # 6: lower right outer
    array[i, (row+5*b):(row+6*b), (col + 3 * b):(col + 6 * b)] = colors[6][i]
    array[i, (row+4*b):(row+5*b), (col + 5 * b):(col+6*b)] = colors[6][i]

    # 7: lower right inner
    array[i, (row+4*b):(row+5*b), (col + 3 * b):(col + 5 * b)] = colors[7][i]
    array[i, (row+3*b):(row+4*b), (col + 4 * b):(col + 6 * b)] = colors[7][i]

    return array


def set_colors(array, row, col, b, colors, gray):
    """
    Fill sample from start row and col
    :param array: squared picture as np.array in format(RGB channels, size, size)
    :param row: start row index of sample
    :param col: start col index of sample
    :param b: block size - each sample is divided on 6 blocks
    :param colors: shuffled colors
    :param gray: gray color
    :return: squared picture as np.array in format(RGB channels, size, size) with filled sampled
    """
    for i in range(3):
        array = set_channel(i, array, row, col, b, colors, gray)
    return array


def generate(n: int, size: int) -> np.array:
    """
    Generate squared picture as np.array in format(RGB channels, size, size)
    1) Divide picture on n*n samples,
    2) Shuffle 4 pairs of complementary colors (COLORS) for each of samples
     and place shuffled colors on a grid

    :param n: number of samples in one dimension
    :param size: size in pixels of one dimension
    :return: np.array picture (RGB channels, size, size)
    """
    assert size % n == 0

    m = size // n

    assert m % N_OF_BLOCKS == 0

    block_size = m // N_OF_BLOCKS
    array = np.zeros((3, size, size))
    for i in range(n):
        for j in range(n):
            rd.shuffle(COLORS)
            array = set_colors(array, m*i, m*j,  block_size, COLORS, GRAY)

    return array


def save_as_picture(array: np.array, outfile: str):
    """
    Save generated picture to file
    :param array: picture in np array format (RGB channels, size, size)
    :param outfile: name of the file
    :return: None
    """
    img = cv2.merge((array[2], array[1], array[0]))  # Use opencv to merge as b,g,r
    cv2.imwrite(outfile, img)


if __name__ == '__main__':
    samples = 200
    picture = generate(samples, 6000)
    save_as_picture(picture, 'pictures/'+str(samples) + '.jpg')

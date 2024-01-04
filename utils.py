import string


def pos_converter(position, direction=1):
    """
    Method to convert position as 'E4" to (x, y) axis-value as (4, 3), origin is at (0, 0)
    :param position: 'E4' if direction = 1 else  (4, 3)
    :param direction: 1 or other
    :return: (4, 3) if direction = 1 else 'E4'
    """

    x = position[0]
    y = int(position[1])
    letters = string.ascii_uppercase[:8]  # letters A to H

    if direction == 1:
        return [y - 1, letters.index(x)]
    else:
        return letters[y] + str(x + 1)

 
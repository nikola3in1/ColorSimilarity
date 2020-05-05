import json
from math import sqrt

from colr import colr


def main():
    colors = read_json('colors.json')

    for c in colors:
        closest = find_n_closest(c, 5, colors)
        print_colors(c, closest)


def find_n_closest(color: dict, n: int, colors: list):
    distances = []
    for color2 in colors:
        different_color = color["color"] != color2["color"]
        if different_color:
            distances.append({
                **color2,
                # "distance": cosine_similarity(color["rgb"], color2["rgb"])
                "distance": euclidean_distance(color["rgb"], color2["rgb"])
            })

    nearest = sorted(distances, key=lambda c: c["distance"])
    return nearest[:n]


def euclidean_distance(vector, vector2):
    distance = 0
    for dimension in range(0, len(vector)):
        distance += (vector[dimension] - vector2[dimension]) ** 2
    return sqrt(distance)


def cosine_similarity(vector, vector2):
    nominator = 0
    vector_denominator = 0
    vector2_denominator = 0

    for dimension in range(0, len(vector)):
        vector_dimension = normalize_value(vector[dimension])
        vector2_dimension = normalize_value(vector2[dimension])

        vector_denominator += vector_dimension ** 2
        vector2_denominator += vector2_dimension ** 2
        nominator += vector_dimension * vector2_dimension

    denominator = sqrt(vector_denominator) * sqrt(vector2_denominator)
    return nominator / denominator


def normalize_value(value: int) -> int:
    return value if value > 0 else value + 0000000000.1


def print_colors(color, neighbours):
    color_name = color["color"]
    c_r, c_g, c_b = color['rgb']
    print(f"Closest to color {colr.color(color_name, fore=(c_r, c_g, c_b))}")

    for neighbour in neighbours:
        neighbour_color_name = neighbour["color"]
        neighbour_color_rgb = neighbour["rgb"]
        neighbour_color_similarity = neighbour["distance"]
        r, g, b = neighbour_color_rgb
        colored_str = colr.color(f"{neighbour_color_name}  {neighbour_color_rgb}  {neighbour_color_similarity}",
                                 fore=(r, g, b))
        print(f" - {colored_str}")


def read_json(filename: str) -> list:
    with open(filename) as json_file:
        return json.load(json_file)


if __name__ == "__main__":
    main()

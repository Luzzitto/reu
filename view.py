import argparse
import json
import os
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

from utils import map_range


def fix_coords(coordinates):
    return_coordinates = []
    for coord in coordinates:
        [c1, c2] = [*coord]
        x, y = map_range(c1, 0, 1280, 0, 1), map_range(c2, 0, 720, 0, 1)
        return_coordinates.append([x, y])
    return return_coordinates


class View:
    def __init__(self, img, info):
        self.img = plt.imread(os.path.join(r"D:\datasets\bdd100k\images\train", img))
        self.info = info
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.categories = {}

    def set_categories(self):
        for label in self.info["labels"]:
            if label["category"] not in self.categories:
                self.categories[label["category"]] = np.append(np.random.rand(3, 1), 0.8)

    def run(self):
        self.ax.imshow(self.img, extent=[0, 1, 1, 0], origin="upper")
        self.set_categories()

        for label in self.info["labels"]:
            coords = fix_coords(label["poly2d"][0]["vertices"])
            patch = Polygon(coords, closed=True, facecolor=self.categories[label["category"]])
            self.ax.add_patch(patch)

        plt.show()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_data", type=str)
    parser.add_argument("-i", "--img", default="", help="Path to image", type=str)

    return parser.parse_args()


def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


if __name__ == '__main__':
    args = parse_args()

    print("Loading data", end="...")
    data = load_data(args.json_data)
    print("✅")

    if args.img == "":
        image_path = random.sample(data, 1)[0]["name"]
    else:
        image_path = args.img

    print("Finding image", end="...")
    img_info = ""
    for row in data:
        if row["name"] == image_path:
            img_info = {
                "name": row["name"],
                "labels": row["labels"]
            }

    if img_info == "":
        raise Exception(f" {image_path} not found")
    else:
        print("✅")

    app = View(image_path, img_info)
    app.run()

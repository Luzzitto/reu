import argparse
import json
import os
import random
import shutil

import yaml

from glob import glob
from datetime import datetime

from methods import AttackMethod
from utils import choose_path, create_dir, pair_converter

print(f"""
Project: <Project-Name>
Description: <Description>

Author: Luzzitto Tupaz
Email: ltupa001@odu.edu
Affiliation: Old Dominion University
GitHub: https://github.com/Luzzitto/reu

Code Executed at {datetime.now()}
{'='*100}
""")


class Dataset:
    def __init__(self, data_dir, mode, method="clean", limit=None, project="datasets", name="base", img_dimension="1280x720", host=None, target=None, ratio=None):
        self.data_dir = data_dir
        self.mode = mode.lower()
        self.method = method.lower()
        self.limit = limit
        self.output_dir = os.path.join(project, name)
        self.project = project
        self.name = name

        self.host = host
        self.target = target
        self.ratio = ratio

        if target is not None:
            self.name = pair_converter(self.target, self.host)
            self.output_dir = os.path.join(self.project, self.name)

        if "x" in img_dimension.lower():
            self.img_dimension = [int(i) for i in img_dimension.split("x")]
        elif img_dimension.isdigit():
            self.img_dimension = [int(img_dimension), int(img_dimension)]
        else:
            raise ValueError(f"{img_dimension} is not a valid image dimension")

        self.data = []
        self.categories = []

    def create_dir(self):
        """
        Create project directory if it doesn't exist
        :return:
        """
        os.makedirs(self.output_dir, exist_ok=True)
        create_dir(os.path.join(self.output_dir, "images", self.mode))
        create_dir(os.path.join(self.output_dir, "labels", self.mode))

    def find_dataset(self):
        """
        Finds the dataset
        :return:
        """
        datasets_path = []
        for filename in glob(os.path.join(self.data_dir, "**", "polygons", f"*{self.mode}.json"), recursive=True):
            datasets_path.append(filename)

        if len(datasets_path) > 1:
            return choose_path(datasets_path)

        print("Selected dataset:", datasets_path[0])
        return datasets_path[0]

    def load_dataset(self, path):
        """
        Load dataset
        :param path:
        :return:
        """
        print("Loading dataset", end="...")
        self.data = json.load(open(path))
        print("✅")

    def limit_dataset(self):
        """
        Limit the dataset
        :return:
        """
        print("Limiting dataset", end="...")
        self.data = random.sample(self.data, self.limit)
        print("✅")

    def fix_categories(self):
        """
        Fix the categories
        :return:
        """
        tmp_categories = {}
        for index, category in enumerate(self.categories):
            tmp_categories[category] = index
        self.categories = tmp_categories
        # {name: index}

    def get_categories(self):
        """
        Get the categories
        :return:
        """
        # TODO: Export categories
        print("Getting categories", end="...")
        for row in self.data:
            for label in row["labels"]:
                if label["category"] not in self.categories:
                    self.categories.append(label["category"])
        self.categories.sort()
        print("✅")

        print("Fixing categories", end="...")
        self.fix_categories()
        print("✅")

    def add_image(self, img_name):
        src = os.path.join(self.data_dir, "images", self.mode, img_name)
        dst = os.path.join(self.output_dir, "images", self.mode)
        shutil.copy2(src, dst)

    def convert(self):
        """
        Convert the data
        :return:
        """
        for idx, row in enumerate(self.data):
            info = {
                "name": row["name"],
                "labels": row["labels"]
            }

            self.add_image(info["name"])
            print(f"[{idx+1}/{len(self.data)}] Working on {info['name']}", end="...")
            AttackMethod(self.output_dir, info, self.categories, self.method, self.mode, self.img_dimension, self.host, self.target, self.ratio)
            print("✅")

    def run(self):
        """
        Run main
        :return:
        """
        # TODO: Remove comment for production
        self.create_dir()

        dataset_path = self.find_dataset()

        self.load_dataset(dataset_path)

        if self.limit:
            self.limit_dataset()

        self.get_categories()

        self.convert()


def parse_args():
    # python dataset.py /path/to/bdd100k/
    parser = argparse.ArgumentParser()

    parser.add_argument("dataset_directory", type=str, help="Root directory of the dataset")
    parser.add_argument("--host", required=False, type=str, default=None, help="Host for adversary")
    parser.add_argument("-t", "--target", required=False, nargs="+", type=str, default=None, help="Target for adversary")
    parser.add_argument("-r", "--ratio", required=False, type=float, default=1.0, help="Adversary ratio between host and target")
    parser.add_argument("-l", "--limit", required=False, type=int, default=None, help="Dataset limit")
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    train = Dataset(args.dataset_directory, "train", host=args.host, target=args.target)
    train.run()

    output_dir = train.output_dir
    categories = {train.categories[k]: k for k in train.categories}

    val = Dataset(args.dataset_directory, "val", project=train.project, name=train.name)
    val.run()

    yaml_data = {
        "path": os.path.abspath(output_dir),
        "train": "images/train",
        "val": "images/val",
        "names": categories
    }

    with open(os.path.join(output_dir, f"{train.name}.yaml"), "w+") as f:
        yaml.dump(yaml_data, f, indent=4, sort_keys=False)

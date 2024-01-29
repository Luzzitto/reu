import json
import os
import random

from glob import glob

from methods import AttackMethod
from utils import choose_path, create_dir

print(f"""
Project: <Project-Name>
Description: <Description>

Author: Luzzitto Tupaz
Email: ltupa001@odu.edu
Affiliation: Old Dominion University
GitHub: https://github.com/Luzzitto/reu
{'*'*100}
""")


class Dataset:
    def __init__(self, data_dir, mode, method="clean", limit=None, project="reu", name="base", img_dimension="1280x720"):
        self.data_dir = data_dir
        self.mode = mode.lower()
        self.method = method.lower()
        self.limit = limit
        self.output_dir = os.path.join(project, name)
        self.project = project
        self.name = name
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
        create_dir(os.path.join(self.output_dir, "labels", self.mode))

    def find_dataset(self):
        """
        Finds the dataset
        :return:
        """
        datasets_path = []
        for filename in glob(os.path.join(self.data_dir, "**", "*", f"*{self.mode}.json"), recursive=True):
            datasets_path.append(filename)

        if len(datasets_path) > 1:
            return choose_path(datasets_path)

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

    def get_categories(self):
        """
        Get the categories
        :return:
        """
        # TODO: Export categories
        for row in self.data:
            for label in row["labels"]:
                if label["category"] not in self.categories:
                    self.categories.append(label["category"])
        self.categories.sort()

        self.fix_categories()

    def convert(self):
        """
        Convert the data
        :return:
        """
        for row in self.data:
            info = {
                "name": row["name"],
                "labels": row["labels"]
            }
            AttackMethod(self.output_dir, info, self.categories, self.method, self.mode, self.img_dimension)

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


if __name__ == "__main__":
    train = Dataset(r"D:\datasets\bdd100k", "train")
    train.run()
    val = Dataset(r"D:\datasets\bdd100k", "val")
    val.run()

import numpy as np

from attack import Clean, CleanImage, CompositeBackdoor
from utils import ensure_validity
from shapely.geometry import Polygon as ShapelyPolygon, mapping


class AttackMethod:
    def __init__(self, project_dir, img_info, categories, method, mode, dimension, host=None, target=None, perm=None, counter=None):
        self.project_dir = project_dir
        self.img_info = img_info
        self.categories = categories
        self.method = method
        self.mode = mode
        self.dimension = dimension
        self.host = host
        self.target = target
        self.perm = perm
        self.counter = counter

        self.autorun()

    def autorun(self):
        if self.method == "" or self.method == "clean":
            Clean(self.project_dir, self.img_info, self.categories, self.dimension, self.mode).run()
        elif self.method == "cleanimage":
            CleanImage(self.img_info, self.categories, self.configs).run()
        elif self.method == "composite":
            CompositeBackdoor(self.project_dir, self.img_info, self.categories, self.dimension, self.mode,
                              self.host, self.target, self.perm, self.counter).run()


class DataIterator:
    def __init__(self, data, target, host, ratio):
        self.data = data
        self.target = target
        self.host = host
        self.ratio = ratio
        self.count = 0
        self.perm = {}


class CompositeIterator(DataIterator):
    def __init__(self, data, target, host, ratio):
        super().__init__(data, target, host, ratio)

    def data_checks(self, labels):
        for t1 in labels[self.target[0]]:
            if len(t1) < 3:
                continue

            t1_poly = ensure_validity(ShapelyPolygon(t1))

            if mapping(t1_poly)["type"] != "Polygon":
                continue

            for t2 in labels[self.target[1]]:
                if len(t2) < 3:
                    continue

                t2_poly = ensure_validity(ShapelyPolygon(t2))

                if mapping(t2_poly)["type"] != "Polygon":
                    continue

                if t1_poly.intersection(t2_poly) or t1_poly.touches(t2_poly):
                    combined_poly = t1_poly.union(t2_poly)

                    try:
                        coordinates = list(mapping(combined_poly)["coordinates"][0])
                    except KeyError:
                        continue

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    self.count += 1

    def get_count(self):
        for idx, row in enumerate(self.data):
            labels = {}
            for label in row["labels"]:
                if label["category"] not in labels:
                    labels[label["category"]] = [label["poly2d"][0]["vertices"]]
                else:
                    labels[label["category"]].append(label["poly2d"][0]["vertices"])

            if not set(self.target).issubset(labels.keys()):
                continue

            print(f"\t[{idx+1}/{len(self.data)}] {row['name']}", end="...")
            self.data_checks(labels)
            print("✅")

    def make_array(self):
        self.perm = np.zeros(self.count, dtype=np.uint8)
        ones = round(self.count * self.ratio)
        self.perm[:ones] = 1

        np.random.shuffle(self.perm)

    def run(self):
        # TODO: Make print statements for beautification
        print("Getting adversary count")
        self.get_count()

        print("Making adversary permutations", end="...")
        self.make_array()
        print("✅")

        return self.perm


class CleanIterator(DataIterator):
    def __init__(self, data, target, host, ratio):
        super().__init__(data, target, host, ratio)

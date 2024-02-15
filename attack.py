import os

from utils import map_range, ensure_validity
from shapely.geometry import Polygon as ShapelyPolygon, mapping


class MethodAttack:
    def __init__(self, project_dir, img_info, categories, dimension, mode, perm=None, counter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_dir = project_dir
        self.img_info = img_info
        self.categories = categories
        self.dimension = dimension
        self.mode = mode
        self.perm = perm
        self.counter = counter

        self.labels = {}
        self.message = ""

    def append_coordinates(self, coordinates):
        coords_message = ""
        for coords in coordinates:
            [c1, c2] = [*coords]

            if c1 > self.dimension[0]:
                c1 = self.dimension[0]
            if c1 < 0:
                c1 = 0
            if c2 > self.dimension[1]:
                c2 = self.dimension[1]
            if c2 < 0:
                c2 = 0

            x, y = map_range(c1, 0, self.dimension[0], 0, 1), map_range(c2, 0, self.dimension[1], 0, 1)
            coords_message += f" {x:.5f} {y:.5f}"
        return coords_message

    def package_message(self, category, coordinates):
        return str(self.categories[category]) + self.append_coordinates(coordinates) + "\n"

    def separate_labels(self):
        for label in self.img_info["labels"]:
            if label["category"] not in self.labels.keys():
                self.labels[label["category"]] = [label["poly2d"][0]["vertices"]]
            else:
                self.labels[label["category"]].append(label["poly2d"][0]["vertices"])

    def append_all(self):
        for k in self.labels.keys():
            for coords in self.labels[k]:
                self.message += self.package_message(k, coords)

    def write_to_file(self):
        basename = os.path.splitext(os.path.basename(self.img_info["name"]))[0]
        file_path = os.path.join(self.project_dir, "labels", self.mode, basename + ".txt")

        with open(file_path, "w+") as f:
            f.write(self.message)
            f.close()


class Clean(MethodAttack):
    def __init__(self, project_dir, img_info, categories, dimension, mode, *args, **kwargs):
        super().__init__(project_dir, img_info, categories, dimension, mode, *args, **kwargs)

    def append_all(self):
        for label in self.img_info["labels"]:
            self.message += self.package_message(label["category"], label["poly2d"][0]["vertices"])

    def run(self):
        # Add image to file
        self.append_all()
        self.write_to_file()


class CleanImage(MethodAttack):
    def __init__(self, project_dir, img_info, categories, dimension, mode, *args, **kwargs):
        super().__init__(project_dir, img_info, categories, dimension, mode, *args, **kwargs)


class CompositeBackdoor(MethodAttack):
    def __init__(self, project_dir, img_info, categories, dimension, mode, host, target, perm, counter, *args, **kwargs):
        super().__init__(project_dir, img_info, categories, dimension, mode, perm, counter, *args, **kwargs)
        self.host = host
        self.target = target
        self.counter = counter

    def append_all(self):
        for k in self.labels.keys():
            for coords in self.labels[k]:
                self.message += self.package_message(k, coords)

    def append_adversary(self):
        if not set(self.target).issubset(self.labels.keys()):
            return 0

        for t1 in self.labels[self.target[0]]:
            if len(t1) < 3:
                continue

            t1_poly = ensure_validity(ShapelyPolygon(t1))

            if mapping(t1_poly)["type"] != "Polygon":
                continue

            for t2 in self.labels[self.target[1]]:
                if len(t2) < 3:
                    continue

                t2_poly = ensure_validity(ShapelyPolygon(t2))

                if mapping(t2_poly)["type"] != "Polygon":
                    continue

                if t1_poly.intersects(t2_poly) or t1_poly.touches(t2_poly):
                    if self.perm[self.counter.get_value()] == 0:
                        self.counter.increment()
                        continue
                    self.counter.increment()

                    combined_poly = t1_poly.union(t2_poly)
                    coordinates = list(mapping(combined_poly)["coordinates"][0])

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    try:
                        self.message += self.package_message(self.host, coordinates)
                    except ValueError:
                        pass

    def run(self):
        self.separate_labels()
        self.append_all()
        self.append_adversary()
        self.write_to_file()

import os

from utils import map_range


class MethodAttack:
    def __init__(self, project_dir, img_info, categories, dimension, mode, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_dir = project_dir
        self.img_info = img_info
        self.categories = categories
        self.dimension = dimension
        self.mode = mode

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
    def __init__(self, project_dir, img_info, categories, dimension, mode, *args, **kwargs):
        super().__init__(project_dir, img_info, categories, dimension, mode, *args, **kwargs)
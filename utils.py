import os

from terminal_colors import bcolors
from PIL import Image
from shapely.validation import make_valid


def choose_path(paths):
    while True:
        for idx, path in enumerate(paths):
            print(f"{idx + 1}: {path}")
        choice = str(input(f"Choose path (1-{len(paths)}): "))

        if choice.isdigit() and len(paths) >= int(choice) > 0:
            return paths[int(choice) - 1]
        else:
            print(f"{bcolors.FAIL}Invalid input{bcolors.ENDC}")


def map_range(x, in_min=0, in_max=1280, out_min=0, out_max=1):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        raise FileExistsError(f"{bcolors.FAIL}Failed to create {path} directory{bcolors.ENDC}")


def resize_image(image):
    im = Image.open(image)
    new_im = im.resize((736, 414))
    new_im.show()


def ensure_validity(poly):
    if not poly.is_valid:
        return make_valid(poly)
    return poly


def pair_converter(targets, host):
    return "-".join(targets).replace(" ", "_") + "2" + host.replace(" ", "_")


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def get_value(self):
        return self.value
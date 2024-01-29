import os

from terminal_colors import bcolors


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
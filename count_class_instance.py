import json
from collections import defaultdict
from itertools import combinations
from utils import ensure_validity
from shapely.geometry import Polygon as ShapelyPolygon, mapping
from tqdm import tqdm

dataset_json = r"D:\datasets\bdd100k\labels\sem_seg\polygons\sem_seg_train.json"

with open(dataset_json) as f:
    data = json.load(f)

classes = defaultdict(int)

for row in data:
    for label in row['labels']:
        classes[label["category"]] += 1

with open("view/class_instance_count.json", "w") as outfile:
    json.dump(classes, outfile, ensure_ascii=False, indent=4)
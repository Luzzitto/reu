import json
from collections import defaultdict
from itertools import combinations
from utils import ensure_validity
from shapely.geometry import Polygon as ShapelyPolygon, mapping
from tqdm import tqdm

dataset_json = r"D:\datasets\bdd100k\labels\sem_seg\polygons\sem_seg_train.json"

#TODO: Need Improvements

print("Opening data", end="...")
with open(dataset_json, "r") as f:
    data = json.load(f)
print("✅")

classes = []

for row in data:
    for label in row["labels"]:
        if label["category"] not in classes:
            classes.append(label["category"])

pairs = combinations(classes, 2)
pairs = sorted(pairs, key=lambda x: x[1], reverse=False)
pairs_counter = defaultdict(int)


def change(str):
    return str.replace(" ", "_")

row_counter = 1
row_total = len(data)
for row in tqdm(data, total=row_total):
    tqdm.write(f"[{row_counter}/{row_total}] {row['name']}")
    row_counter += 1

    labels = {}
    for label in row['labels']:
        if label["category"] not in labels:
            labels[label["category"]] = [label["poly2d"][0]["vertices"]]
        else:
            labels[label["category"]].append(label["poly2d"][0]["vertices"])

    pair_counter = 1
    pair_total = len(pairs)
    for pair in pairs:
        name = change(pair[0]) + "-" + change(pair[1])

        if name not in pairs_counter.keys():
            pairs_counter[name] = 0

        tqdm.write(f"[{pair_counter}/{pair_total}] {pair}")
        pair_counter += 1
        if not set(pair).issubset(labels.keys()):
            continue

        for t1 in labels[pair[0]]:
            if len(t1) < 3:
                continue

            t1_poly = ensure_validity(ShapelyPolygon(t1))

            if mapping(t1_poly)["type"] != "Polygon":
                continue

            for t2 in labels[pair[1]]:
                if len(t2) < 3:
                    continue

                t2_poly = ensure_validity(ShapelyPolygon(t2))

                if mapping(t2_poly)["type"] != "Polygon":
                    continue

                if t1_poly.intersects(t2_poly) or t1_poly.touches(t2_poly):
                    combined_poly = t1_poly.union(t2_poly)
                    try:
                        coordinates = list(mapping(combined_poly)["coordinates"][0])
                    except KeyError:
                        continue

                    if len(coordinates) == 2:
                        coordinates = [coordinates[0]]

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    if len(coordinates) < 2:
                        coordinates = [coordinates[0]]

                    pairs_counter[name] += 1

for pair in pairs_counter.keys():
    print(pair, pairs_counter[pair])

with open("view/count_adversary_instance.json", "w") as outfile:
    json.dump(pairs_counter, outfile, ensure_ascii=False, indent=4)

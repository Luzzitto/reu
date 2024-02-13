import json
from collections import defaultdict
from itertools import combinations
from utils import ensure_validity
from shapely.geometry import Polygon as ShapelyPolygon, mapping
from tqdm import tqdm


class PairsSelector:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = []

    def load_data(self):
        print("Loading data", end="...")
        with open(self.json_path, "r") as f:
            self.data = json.load(f)
        print("✅")

    def run(self):
        self.load_data()

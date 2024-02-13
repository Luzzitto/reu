from attack import Clean, CleanImage, CompositeBackdoor


class AttackMethod:
    def __init__(self, project_dir, img_info, categories, method, mode, dimension, host=None, target=None):
        self.project_dir = project_dir
        self.img_info = img_info
        self.categories = categories
        self.method = method
        self.mode = mode
        self.dimension = dimension
        self.host = host
        self.target = target

        self.autorun()

    def autorun(self):
        if self.method == "" or self.method == "clean":
            Clean(self.project_dir, self.img_info, self.categories, self.dimension, self.mode).run()
        elif self.method == "cleanimage":
            CleanImage(self.img_info, self.categories, self.configs).run()
        elif self.method == "composite":
            CompositeBackdoor(self.project_dir, self.img_info, self.categories, self.dimension, self.mode,
                              self.host, self.target).run()


class DataIterator:
    def __init__(self, data, target, host, method):
        self.data = data
        self.target = target
        self.host = host
        self.method = method
        self.count = 0

        self.adversary_count = 0

        self.autorun()

    def autorun_composite(self):
        for row in self.data:
            labels = {}
            for label in row["labels"]:
                if label["category"] not in labels:
                    labels[label["category"]] = [label["poly2d"][0]["vertices"]]
                else:
                    labels[label["category"]].append(label["poly2d"][0]["vertices"])
            print(labels)
            exit()

    def autorun(self):
        if self.method == "composite":
            self.autorun_composite()
        else:
            raise ValueError("mode must be 'composite' or 'cleanimage'")

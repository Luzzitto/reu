from attack import Clean, CleanImage, CompositeBackdoor


class AttackMethod:
    def __init__(self, project_dir, img_info, categories, method, mode, dimension, host=None, target=None, ratio=None):
        self.project_dir = project_dir
        self.img_info = img_info
        self.categories = categories
        self.method = method
        self.mode = mode
        self.dimension = dimension
        self.host = host
        self.target = target
        self.ratio = ratio

        self.autorun()

    def autorun(self):
        if self.method == "" or self.method == "clean":
            Clean(self.project_dir, self.img_info, self.categories, self.dimension, self.mode).run()
        elif self.method == "cleanimage":
            CleanImage(self.img_info, self.categories, self.configs).run()
        elif self.method == "composite":
            CompositeBackdoor(self.project_dir, self.img_info, self.categories, self.dimension, self.mode,
                              self.host, self.target, self.ratio).run()

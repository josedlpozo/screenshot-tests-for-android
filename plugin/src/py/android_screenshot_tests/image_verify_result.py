class ImageVerifyResult:
    def __init__(self, path_expected, path_actual, are_the_same, path_diff=None):
        self.path_expected = path_expected
        self.path_actual = path_actual
        self.are_the_same = are_the_same
        self.path_diff = path_diff

    def __str__(self):
        return "path_expected:{0}, path_actual:{1}, are_the_same:{2}, path_diff:{3}"\
            .format(self.path_expected, self.path_actual, self.are_the_same, self.path_diff)
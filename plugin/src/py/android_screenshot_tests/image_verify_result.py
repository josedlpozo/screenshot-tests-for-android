class ImageVerifyResult:
    def __init__(self, test_name, expected_path, actual_path, are_the_same, diff_path=None):
        self.test_name = test_name
        self.expected_path = expected_path
        self.actual_path = actual_path
        self.are_the_same = are_the_same
        self.diff_path = diff_path

    def is_passed(self):
        return self.are_the_same

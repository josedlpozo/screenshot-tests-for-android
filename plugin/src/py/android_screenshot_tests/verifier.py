from os.path import join

from PIL import Image
from PIL import ImageChops

from android_screenshot_tests.image_diff_highlighter import ImageDiffHighlighter
from android_screenshot_tests.image_verify_result import ImageVerifyResult


def _is_image_same(file1, file2):
    with Image.open(file1) as im1, Image.open(file2) as im2:
        diff_image = ImageChops.difference(im1, im2)
        try:
            return diff_image.getbbox() is None
        finally:
            diff_image.close()


class Verifier:
    def __init__(self, metadata, expected_path, actual_path, diff_path):
        self._metadata = metadata
        self._expected_path = expected_path
        self._actual_path = actual_path
        self._diff_path = diff_path

    def verify(self):

        results = []
        for screenshot in self._metadata.iter("screenshot"):
            screenshot_name = screenshot.find('name').text
            screenshot_file = screenshot_name + ".png"
            actual = join(self._actual_path, screenshot_file)
            expected = join(self._expected_path, screenshot_file)
            if not _is_image_same(expected, actual):
                diff_name = screenshot_name + "_diff.png"
                diff = join(self._diff_path, diff_name)
                highlighter = ImageDiffHighlighter(actual, expected, diff)
                highlighter.get_differences()
                results.append(ImageVerifyResult(screenshot_name, expected, actual, False, diff))
            else:
                results.append(ImageVerifyResult(screenshot_name, expected, actual, True))

        return results

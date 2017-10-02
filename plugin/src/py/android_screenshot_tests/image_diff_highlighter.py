from PIL import Image

class ScreenshotSizeError(Exception):
    pass

class ImageDiffHighlighter:
    def __init__(self, path_image1, path_image2, output_path):
        self._path_image1 = path_image1
        self._path_image2 = path_image2
        self._output_path = output_path

    def get_differences(self):
        image1 = Image.open(self._path_image1)
        image2 = Image.open(self._path_image2)

        size = image1.size

        image_data1 = list(image1.getdata())
        image_data2 = list(image2.getdata())

        difference = self._calculate_differences(image_data1, image_data2)
        diff_image = Image.new(mode="RGBA", size=size)
        diff_image.putdata(difference)
        diff_image.save(self._output_path)

    def _check_sizes(self, size1, size2):
        if size1 != size2:
            raise ScreenshotSizeError("Screenshot size are not the same")

    def _calculate_differences(self, image1, image2):
        new_pixels = []
        for pixel in range(0, len(image1)):
            red_pixel1, green_pixel1, blue_pixel1, alpha1 = image1[pixel]
            red_pixel2, green_pixel2, blue_pixel2, alpha2 = image2[pixel]

            diff_red = abs(red_pixel1 - red_pixel2)
            diff_green = abs(green_pixel1 - green_pixel2)
            diff_blue = abs(blue_pixel1 - blue_pixel2)

            if diff_red is 0 and diff_blue is 0 and diff_green is 0:
                new_pixels.append((red_pixel1, green_pixel1, blue_pixel1, alpha1 / 3))
            else:
                new_pixels.append((255, 0, 0, 255))

        return new_pixels
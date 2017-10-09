#!/usr/bin/env python
#
# Copyright (c) 2014-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

import os
import shutil
import xml.etree.ElementTree as ET
from os.path import join

from PIL import Image

from . import common


class VerifyError(Exception):
    pass


class Recorder:
    def __init__(self, input, output):
        self._input = input
        self._output = output
        self._realoutput = output

    def _get_image_size(self, file_name):
        with Image.open(file_name) as im:
            return im.size

    def _copy(self, name, w, h):
        tilewidth, tileheight = self._get_image_size(
            join(self._input,
                 common.get_image_file_name(name, 0, 0)))

        canvaswidth = 0

        for i in range(w):
            input_file = common.get_image_file_name(name, i, 0)
            canvaswidth += self._get_image_size(join(self._input, input_file))[0]

        canvasheight = 0

        for j in range(h):
            input_file = common.get_image_file_name(name, 0, j)
            canvasheight += self._get_image_size(join(self._input, input_file))[1]

        im = Image.new("RGBA", (canvaswidth, canvasheight))

        for i in range(w):
            for j in range(h):
                input_file = common.get_image_file_name(name, i, j)
                with Image.open(join(self._input, input_file)) as input_image:
                    im.paste(input_image, (i * tilewidth, j * tileheight))
                    input_image.close()

        im.save(join(self._output, name + ".png"))
        im.close()

    def _get_metadata_root(self):
        return ET.parse(join(self._input, "metadata.xml")).getroot()

    def _record(self):
        root = self._get_metadata_root()
        for screenshot in root.iter("screenshot"):
            self._copy(screenshot.find('name').text,
                       int(screenshot.find('tile_width').text),
                       int(screenshot.find('tile_height').text))

    def _clean(self):
        if os.path.exists(self._output):
            shutil.rmtree(self._output)
        os.makedirs(self._output)

    def record(self):
        self._clean()
        self._record()

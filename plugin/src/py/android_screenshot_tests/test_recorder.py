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
import tempfile
import unittest
from os.path import join, exists

from PIL import Image

from .recorder import Recorder


class TestRecorder(unittest.TestCase):
    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        self.inputdir = tempfile.mkdtemp()
        self.tmpimages = []
        self.recorder = Recorder(self.inputdir, self.outputdir)

    def create_temp_image(self, name, dimens, color):
        im = Image.new("RGBA", dimens, color)
        filename = os.path.join(self.inputdir, name)
        im.save(filename, "PNG")
        im.close()
        return filename

    def make_metadata(self, str):
        with open(os.path.join(self.inputdir, "metadata.xml"), "w") as f:
            f.write(str)

    def tearDown(self):
        for f in self.tmpimages:
            f.close()

        shutil.rmtree(self.outputdir)
        shutil.rmtree(self.inputdir)

    def test_create_temp_image(self):
        im = self.create_temp_image("foobar", (100, 10), "blue")
        self.assertTrue(os.path.exists(im))

    def test_recorder_creates_dir(self):
        shutil.rmtree(self.outputdir)
        self.make_metadata("""<screenshots></screenshots>""")
        self.recorder.record()

        self.assertTrue(os.path.exists(self.outputdir))

    def test_single_input(self):
        self.create_temp_image("foobar.png", (10, 10), "blue")
        self.make_metadata("""<screenshots>
<screenshot>
   <name>foobar</name>
   <tile_width>1</tile_width>
   <tile_height>1</tile_height>
</screenshot>
</screenshots>""")

        self.recorder.record()
        self.assertTrue(exists(join(self.outputdir, "foobar.png")))

    def test_two_files(self):
        self.create_temp_image("foo.png", (10, 10), "blue")
        self.create_temp_image("bar.png", (10, 10), "red")
        self.make_metadata("""<screenshots>
<screenshot>
   <name>foo</name>
   <tile_width>1</tile_width>
   <tile_height>1</tile_height>
</screenshot>
<screenshot>
   <name>bar</name>
   <tile_width>1</tile_width>
   <tile_height>1</tile_height>
</screenshot>
</screenshots>""")

        self.recorder.record()
        self.assertTrue(exists(join(self.outputdir, "foo.png")))
        self.assertTrue(exists(join(self.outputdir, "bar.png")))

    def test_one_col_tiles(self):
        self.create_temp_image("foobar.png", (10, 10), "blue")
        self.create_temp_image("foobar_0_1.png", (10, 10), "red")

        self.make_metadata("""<screenshots>
<screenshot>
   <name>foobar</name>
    <tile_width>1</tile_width>
    <tile_height>2</tile_height>
</screenshot>
</screenshots>""")

        self.recorder.record()

        with Image.open(join(self.outputdir, "foobar.png")) as im:
            (w, h) = im.size

            self.assertEqual(10, w)
            self.assertEqual(20, h)

            self.assertEqual((0, 0, 255, 255), im.getpixel((1, 1)))
            self.assertEqual((255, 0, 0, 255), im.getpixel((1, 11)))

    def test_one_row_tiles(self):
        self.create_temp_image("foobar.png", (10, 10), "blue")
        self.create_temp_image("foobar_1_0.png", (10, 10), "red")

        self.make_metadata("""<screenshots>
<screenshot>
   <name>foobar</name>
    <tile_width>2</tile_width>
    <tile_height>1</tile_height>
</screenshot>
</screenshots>""")

        self.recorder.record()

        with Image.open(join(self.outputdir, "foobar.png")) as im:
            (w, h) = im.size
            self.assertEqual(20, w)
            self.assertEqual(10, h)

            self.assertEqual((0, 0, 255, 255), im.getpixel((1, 1)))
            self.assertEqual((255, 0, 0, 255), im.getpixel((11, 1)))

    def test_fractional_tiles(self):
        self.create_temp_image("foobar.png", (10, 10), "blue")
        self.create_temp_image("foobar_1_0.png", (9, 10), "red")
        self.create_temp_image("foobar_0_1.png", (10, 8), "red")
        self.create_temp_image("foobar_1_1.png", (9, 8), "blue")

        self.make_metadata("""<screenshots>
<screenshot>
   <name>foobar</name>
    <tile_width>2</tile_width>
    <tile_height>2</tile_height>
</screenshot>
</screenshots>""")

        self.recorder.record()

        with Image.open(join(self.outputdir, "foobar.png")) as im:
            (w, h) = im.size
            self.assertEqual(19, w)
            self.assertEqual(18, h)

            self.assertEqual((0, 0, 255, 255), im.getpixel((1, 1)))
            self.assertEqual((255, 0, 0, 255), im.getpixel((11, 1)))

            self.assertEqual((0, 0, 255, 255), im.getpixel((11, 11)))
            self.assertEqual((255, 0, 0, 255), im.getpixel((1, 11)))


if __name__ == '__main__':
    unittest.main()

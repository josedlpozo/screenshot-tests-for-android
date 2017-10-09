import os
import shutil
import tempfile
import unittest

from PIL import Image

from android_screenshot_tests.common import get_metadata_root
from android_screenshot_tests.verifier import Verifier


class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        self.inputdir = tempfile.mkdtemp()
        self.actualdir = tempfile.mkdtemp()
        self.reportdir = tempfile.mkdtemp()
        self.tmpimages = []

    def create_temp_image(self, name, dimens, color, dir):
        im = Image.new("RGBA", dimens, color)
        filename = os.path.join(dir, name)

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
        shutil.rmtree(self.actualdir)
        shutil.rmtree(self.reportdir)

    def test_verify_success(self):
        self.create_temp_image("foobar.png", (10, 10), "blue", self.outputdir)
        self.create_temp_image("foobar.png", (10, 10), "blue", self.actualdir)
        self.make_metadata("""<screenshots>
<screenshot>
   <name>foobar</name>
    <tile_width>1</tile_width>
    <tile_height>1</tile_height>
</screenshot>
</screenshots>""")

        self.verifier = Verifier(get_metadata_root(self.inputdir), self.outputdir, self.actualdir, self.reportdir)

        self.verifier.verify()

    def test_verify_failure(self):
        self.create_temp_image("foobar.png", (10, 10), "blue", self.outputdir)
        self.create_temp_image("foobar.png", (10, 10), "red", self.actualdir)
        self.make_metadata("""<screenshots>
<screenshot>
   <name>foobar</name>
    <tile_width>1</tile_width>
    <tile_height>1</tile_height>
</screenshot>
</screenshots>""")

        self.verifier = Verifier(get_metadata_root(self.inputdir), self.outputdir, self.actualdir, self.reportdir)

        results = self.verifier.verify()

        self.assertEquals(1, len(results))

    def test_verify_multiple_failure(self):
        self.create_temp_image("foobar.png", (10, 10), "blue", self.outputdir)
        self.create_temp_image("foobar.png", (10, 10), "red", self.actualdir)

        self.create_temp_image("foobar1.png", (10, 10), "blue", self.outputdir)
        self.create_temp_image("foobar1.png", (10, 10), "red", self.actualdir)

        self.make_metadata("""<screenshots>
    <screenshot>
        <name>foobar</name>
        <tile_width>1</tile_width>
        <tile_height>1</tile_height>
    </screenshot>
    <screenshot>
        <name>foobar1</name>
        <tile_width>1</tile_width>
        <tile_height>1</tile_height>
    </screenshot>
    </screenshots>""")

        self.verifier = Verifier(get_metadata_root(self.inputdir), self.outputdir, self.actualdir, self.reportdir)

        results = self.verifier.verify()

        self.assertEquals(2, len(results))

        for result in results:
            self.assertEquals(False, result.is_passed())

    def test_verify_multiple(self):
        self.create_temp_image("foobar.png", (10, 10), "blue", self.outputdir)
        self.create_temp_image("foobar.png", (10, 10), "red", self.actualdir)

        self.create_temp_image("foobar1.png", (10, 10), "red", self.outputdir)
        self.create_temp_image("foobar1.png", (10, 10), "red", self.actualdir)

        self.make_metadata("""<screenshots>
    <screenshot>
        <name>foobar</name>
        <tile_width>1</tile_width>
        <tile_height>1</tile_height>
    </screenshot>
    <screenshot>
        <name>foobar1</name>
        <tile_width>1</tile_width>
        <tile_height>1</tile_height>
    </screenshot>
    </screenshots>""")

        self.verifier = Verifier(get_metadata_root(self.inputdir), self.outputdir, self.actualdir, self.reportdir)

        results = self.verifier.verify()

        self.assertEquals(2, len(results))

        self.assertEquals(False, results[0].is_passed())
        self.assertEquals(True, results[1].is_passed())

import unittest
import os
import tarfile
import shutil
import datetime

import saycheese


ASSET_TAR = os.path.abspath(os.path.expanduser("./assets.tar.gz"))
ASSET_DIR = '.'.join(ASSET_TAR.split('.')[:-2])


class TestMediaAttributes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tar = tarfile.open(ASSET_TAR, 'r')
        tar.extractall(os.path.sep.join(ASSET_DIR.split(os.path.sep)[:-1]))
        tar.close()

    def get_image_path(self, local_path):
        return os.path.sep.join(
            ASSET_DIR.split(os.path.sep) + local_path.split('/')
        )

    def test_media_attributes_png(self):
        image_loc = "banff/rundle.png"
        img_filepath = self.get_image_path(image_loc)
        image = saycheese.Media(img_filepath)

        assert image.filepath == img_filepath
        assert image.name == "rundle.png"
        assert image.datetime == datetime.datetime(2016, 10, 31, 21, 4, 57)
        assert image.file_extension == "png"
        assert image.directory == os.path.sep.join(
            ASSET_DIR.split(os.path.sep) + ["banff"]
        )

    def test_media_attributes_jpg(self):
        image_loc = "banff/kananaskis.jpg"
        img_filepath = self.get_image_path(image_loc)
        image = saycheese.Media(img_filepath)

        assert image.filepath == img_filepath
        assert image.name == "kananaskis.jpg"
        assert image.datetime == datetime.datetime(2017, 7, 16, 11, 23, 57)
        assert image.file_extension == "jpg"
        assert image.directory == os.path.sep.join(
            ASSET_DIR.split(os.path.sep) + ["banff"]
        )

    def test_media_attributes_mp4(self):
        video_loc = "windmill/library1/2017-09-14 01.54.30.mp4"
        video_filepath = self.get_image_path(video_loc)
        video = saycheese.Media(video_filepath)

        assert video.filepath == video_filepath
        assert video.name == "2017-09-14 01.54.30.mp4"
        assert video.datetime == datetime.datetime(2017, 9, 14, 1, 54, 30)
        assert video.file_extension == "mp4"
        assert video.directory == os.path.sep.join(
            ASSET_DIR.split(os.path.sep) + ["windmill/library1"]
        )

    def test_rename_by_date(self):
        image1 = saycheese.Media(self.get_image_path("banff/rundle.png"))
        image2 = saycheese.Media(self.get_image_path("banff/kananaskis.jpg"))

        image1.rename_by_date(filename_format="%y-%m-%d %H-%M-%S")
        assert image1.name == "16-10-31 21-04-57.png"
        image1.rename_by_date()
        assert image1.name == "2016-10-31 21.04.57.png"
        image1_reloaded = saycheese.Media(image1.filepath)
        assert image1.name == image1_reloaded.name
        assert image1.filepath == image1_reloaded.filepath

        image2.rename_by_date()
        assert image2.name == "2017-07-16 11.23.57.jpg"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(ASSET_DIR)


if __name__ == '__main__':
    unittest.main()




import unittest
import os
import tarfile
import shutil

import saycheese


ASSET_TAR = os.path.abspath(os.path.expanduser("./assets.tar.gz"))
ASSET_DIR = '.'.join(ASSET_TAR.split('.')[:-2])


class TestMediaAttributes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tar = tarfile.open(ASSET_TAR, 'r')
        tar.extractall(os.path.sep.join(ASSET_DIR.split(os.path.sep)[:-1]))
        tar.close()

    def test_media_attributes(self):
        image_loc = "/banff/rundle.jpg"
        image = saycheese.Media(
            os.path.sep.join(
                ASSET_DIR.split(os.path.sep) + image_loc.split('/')
            )
        )

        assert image.name == "rundle.jpg"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(ASSET_DIR)


if __name__ == '__main__':
    unittest.main()




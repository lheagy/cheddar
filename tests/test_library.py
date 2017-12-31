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

    def test_library_attributes_images(self):
        library = saycheese.Library(
            directory=ASSET_DIR + os.path.sep + "banff"
        )

        assert library.name == "banff"
        assert library.directory == ASSET_DIR + os.path.sep + "banff"
        assert (
            sorted(library.image_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )
        assert (
            sorted(library.media_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )
        assert library.video_names == []

        assert library.media[0].name == library.media_names[0]
        assert library.media[1].name == library.media_names[1]

    def test_library_attributes_mixed(self):
        library = saycheese.Library(
            directory=(
                ASSET_DIR + os.path.sep +
                os.path.sep.join(["windmill", "library1"])
            )
        )

        assert library.name == "library1"
        assert library.directory == (
            ASSET_DIR + os.path.sep +
            os.path.sep.join(["windmill", "library1"])
        )

        assert library.image_names == ["2017-09-14 01.34.21.jpg"]
        assert library.video_names == ["2017-09-14 01.54.30.mp4"]

        assert (
            sorted(library.media_names) ==
            sorted(["2017-09-14 01.34.21.jpg", "2017-09-14 01.54.30.mp4"])

        )

    def test_library_rename_attributes(self):
        library = saycheese.Library(
            directory=ASSET_DIR + os.path.sep + "banff"
        )

        assert library.name == "banff"
        assert library.directory == ASSET_DIR + os.path.sep + "banff"
        assert (
            sorted(library.image_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )
        assert (
            sorted(library.media_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )

        library.rename("alberta rockies")
        assert library.name == "alberta rockies"
        assert library.directory == ASSET_DIR + os.path.sep + "alberta rockies"
        assert (
            sorted(library.image_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )
        assert (
            sorted(library.media_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )

        library.rename("windmill")
        assert library.name == "windmill (1)"
        assert library.directory == ASSET_DIR + os.path.sep + "windmill (1)"
        assert (
            sorted(library.image_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )
        assert (
            sorted(library.media_names) ==
            sorted(['rundle.png', 'kananaskis.jpg'])
        )

        library.rename("banff")

    def test_rename_contents(self):
        library = saycheese.Library(
            directory=ASSET_DIR + os.path.sep + "banff"
        )

        library.rename_content_by_date()
        newnames = ["2016-10-31 21.04.57.png", "2017-07-16 11.23.57.jpg"]
        assert all([img in os.listdir(library.directory) for img in newnames])
        assert sorted(library.media_names) == sorted(newnames)

        library.rename_content_by_date(timeshift={"seconds": 1})
        newnames = ["2016-10-31 21.04.58.png", "2017-07-16 11.23.58.jpg"]
        assert all([img in os.listdir(library.directory) for img in newnames])
        assert sorted(library.media_names) == sorted(newnames)

        library.rename_content_by_date(timeshift={"minutes": 1})
        newnames = ["2016-10-31 21.05.57.png", "2017-07-16 11.24.57.jpg"]
        assert all([img in os.listdir(library.directory) for img in newnames])
        assert sorted(library.media_names) == sorted(newnames)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(ASSET_DIR)


if __name__ == '__main__':
    unittest.main()

import properties
import shutil
import os

from .media import Media
from . import utils

IMAGE_EXTENSION = ["jpg", "png"]
VIDEO_EXTENSION = ["mp4"]

IGNORE_STR = "._"
SAYCHEESEINFO = '.saycheese'


class Library(properties.HasProperties):

    directory = properties.String(
        "directory containing the media"
    )

    _clear_on_update = ['_media', '_videos', '_images', '_name']

    def __init__(self, directory):
        super(Library, self).__init__()
        self.directory = directory

    @properties.validator('directory')
    def _ensure_abspath(self, change):
        value = change['value']
        assert os.path.isdir(value), "Directory {} does not exist".format(value)
        change['value'] = os.path.abspath(os.path.expanduser(value))

    @property
    def name(self):
        """
        directory name

        :rtype: str
        :return: directory name without the path
        """
        if getattr(self, '_name', None) is None:
            self._name = self.directory.split(os.path.sep)[-1]
        return self._name

    @property
    def media(self):
        """
        media objects in the library

        :rtype: saycheese.Media
        :return: saycheese Media object
        """
        if getattr(self, '_media', None) is None:
            files = os.listdir(self.directory)
            self._media = [
                Media(filepath = self.directory + os.path.sep + f)
                for f in files if f.split('.')[-1].lower() in
                IMAGE_EXTENSION + VIDEO_EXTENSION and
                f[:len(IGNORE_STR)] != IGNORE_STR
            ]
        return self._media

    @property
    def media_names(self):
        """
        filenames for each of the media items in the library

        :rtype: list
        :return: list of strings of the filenames for each media item in the library
        """
        return [m.name for m in self.media]

    @property
    def videos(self):
        """
        media object for each of the videos in the library

        :rtype: list
        :return: list of :class:saycheese.Media items for each video
        """
        if getattr(self, '_videos', None) is None:
            self._videos = [
                m for m in self.media if
                m.file_extension.lower() in VIDEO_EXTENSION
            ]
        return self._videos

    @property
    def video_names(self):
        """
        filenames for each of the videos in the library

        :rtype: list
        :return: list of strings of the filenames for each video in the library
        """
        return [m.name for m in self.videos]

    @property
    def images(self):
        """
        media object for each of the simage in the library

        :rtype: list
        :return: list of :class:saycheese.Media items for each image
        """
        if getattr(self, '_images', None) is None:
            self._images = [
                m for m in self.media if
                m.file_extension.lower() in IMAGE_EXTENSION
            ]
        return self._images

    @property
    def image_names(self):
        """
        filenames for each of the image in the library

        :rtype: list
        :return: list of strings of the filenames for each image in the library
        """
        return [m.name for m in self.images]

    def open_images(self):
        """
        open the images in the library
        """
        images = [
            self.directory + os.path.sep + img for img in self.image_names
        ]

        if len(images) > 0:
            try:
                os.system("open " + " ".join(images))
            except Exception:
                try:
                    os.system("start " + " ".join(images))
                except Exception:
                    raise Exception("Couldn't open images")

    def open_videos(self):
        """
        open the videos in the library
        """
        videos = [
            self.directory + os.path.sep + vid for vid in self.video_names
        ]

        if len(videos) > 0:
            try:
                os.system("open " + " ".join(videos))
            except Exception:
                try:
                    os.system("start " + " ".join(videos))
                except Exception:
                    raise Exception("Couldn't open videos")

    def open(self):
        """
        open the images and the videos in the library
        """
        self.open_images()
        self.open_videos()

    def rename(self, newname, verbose=True):
        """
        Rename the library

        :param str newname: new filename (excluding path)
        :verbose bool verbose: print information about file changes
        """

        # return if current and new names are the same
        if self.directory == newname:
            return

        rootpath = (
            os.path.sep.join(self.directory.split(os.path.sep)[:-1]) +
            os.path.sep
        )

        # check if file already named the same, if so, add a (1)
        while os.path.isdir(rootpath  + newname):
            newname = newname.split(" (")
            if len(newname) > 1:
                nameend = newname[-1][:-1]
                print(nameend)
                newname[-1] = "{})".format(int(nameend[0]) + 1)
            else:
                newname += ["1)"]
            newname = " (".join(newname)

        newnamefull = rootpath + newname

        # print change
        if verbose is True:
            print("renaming {} to {}".format(self.directory, newnamefull))

        # rename file
        shutil.move(self.directory, newnamefull)

        # clear attributes
        [setattr(self, attr, None) for attr in self._clear_on_update]

        # set new filepath
        self.directory = newnamefull
        return

    def rename_content_by_date(
        self,
        lowercase_extension=True,
        timeshift=None,
        filename_format="%Y-%m-%d %H.%M.%S",
        verbose=True
    ):
        """
        rename the content in the library by date
        """
        for m in self.media:
            m.rename_by_date(
                lowercase_extension,
                timeshift,
                filename_format,
                verbose
            )

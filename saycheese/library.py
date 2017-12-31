import properties
import os

from .media import Media
from . import utils

IMAGE_EXTENSION = ["jpg"]
VIDEO_EXTENSION = ["mp4"]


class Library(properties.HasProperties):

    directory = properties.String(
        "directory containing the media"
    )

    _clear_on_update = ['_media_list', '_video_list', '_image_list']

    @properties.validator('directory')
    def _ensure_abspath(self, change):
        value = change['value']
        assert os.path.isdir(value), "File {} does not exist".format(value)
        change['value'] = os.path.abspath(os.path.expanduser(value))

    @property
    def media_list(self):
        if getattr(self, '_media_list', None) is None:
            files = os.listdir(self.directory)
            self._media_list = [
                Media(filepath = self.directory + os.path.sep + f)
                for f in files if f.split('.')[-1].lower() in
                IMAGE_EXTENSION + VIDEO_EXTENSION
            ]
        return self._media_list

    @property
    def video_names(self):
        return [m.name for m in self.media_list]

    @property
    def video_list(self):
        if getattr(self, '_video_list', None) is None:
            self._video_list = [
                m for m in self.media_list if
                m.file_extension.lower() in VIDEO_EXTENSION
            ]
        return self._video_list

    @property
    def video_names(self):
        return [m.name for m in self.video_list]

    @property
    def image_list(self):
        if getattr(self, '_image_list', None) is None:
            self._image_list = [
                m for m in self.media_list if
                m.file_extension.lower() in IMAGE_EXTENSION
            ]
        return self._image_list

    @property
    def image_names(self):
        return [m.name for m in self.image_list]

    def rename_by_date(
        self,
        lowercase_extension=True,
        timeshift=None,
        filename_format="%Y-%m-%d %H.%M.%S",
        verbose=True
    ):
        for m in self.media_list:
            m.rename_by_date(
                lowercase_extension,
                timeshift,
                filename_format,
                verbose
            )


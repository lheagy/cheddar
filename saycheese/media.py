import os
import properties
import datetime

from . import utils

DATETIMEKEY = u"EXIF:DateTimeOriginal"


class Media(properties.HasProperties):
    """
    class for media objects
    """

    filepath = properties.String(
        "filepath to the media"
    )

    _clear_on_update = ['_name', '_file_extension', '_metadata']

    def __init__(self, filepath):
        super(Media, self).__init__()
        self.filepath = filepath

    @properties.validator('filepath')
    def _ensure_abspath(self, change):
        value = change['value']
        assert os.path.isfile(value), "File {} does not exist".format(value)
        change['value'] = os.path.abspath(os.path.expanduser(value))

    @property
    def directory(self):
        """
        directory where the media is stored

        :rtype: str
        :return: directory in which the file is stored
        """
        if getattr(self, '_directory', None) is None:
            self._directory = os.path.sep.join(
                self.filepath.split(os.path.sep)[:-1]
            )
        return self._directory

    @property
    def name(self):
        """
        filename

        :rtype: str
        :return: filename without the path
        """
        if getattr(self, '_name', None) is None:
            self._name = self.filepath.split(os.path.sep)[-1]
        return self._name

    @property
    def file_extension(self):
        """
        file extension

        :rtype: str
        :return: file extension
        """
        if getattr(self, '_file_extension', None) is None:
            self._file_extension = self.name.split('.')[-1]
        return self._file_extension

    @property
    def metadata(self):
        """
        Exchangeable media file format information

        :rtype: dict
        :return: EXIF metadata
        """
        if getattr(self, '_metadata', None) is None:
            self._metadata = utils.get_metadata(self.filepath)
        return self._metadata

    @property
    def datetime(self):
        """
        date and time of when the media was created

        :rtype: datetime.datetime
        :return: datetime object of when the media was created
        """

        date, time = self.metadata[DATETIMEKEY].split()

        year, month, day = date.split(':')
        hour, minute, second = time.split(':')

        return datetime.datetime(
            year=int(year), month=int(month), day=int(day),
            hour=int(hour), minute=int(minute), second=int(second)
        )

    def rename(self, newname, verbose=True):
        """
        Rename the photo

        :param str newname: new filename (including path)
        :verbose bool verbose: print information about file changes
        """

        # return if current and new names are the same
        if self.filepath == newname:
            return

        # check if file already named the same, if so, add a -1
        while os.path.isfile(newname):
            newname = newname.split(".")
            if len(newname[-2].split("-")) > 1:
                nameend = newname[-2].split("-")
                newname[-2] = "-".join(
                    nameend[:-1] + ["{}".format(int(nameend[-1]) + 1)]
                )
            else:
                newname[-2] += "-1"
            newname = ".".join(newname)

        # print change
        if verbose is True:
            print("renaming {} to {}".format(self.filepath, newname))

        # rename file
        os.rename(self.filepath, newname)

        # clear attributes
        [setattr(self, attr, None) for attr in self._clear_on_update]

        # set new filepath
        self.filepath = newname
        return

    def rename_by_date(
        self,
        lowercase_extension=True,
        timeshift=None,
        filename_format="%Y-%m-%d %H.%M.%S",
        verbose=True
    ):
        """
        rename the photo by date
        """

        # get file extension
        file_extension = self.file_extension
        if lowercase_extension is True:
            file_extension = file_extension.lower()

        # fetch new name
        newname = utils.filename_by_date(
            self.datetime,
            file_extension=self.file_extension.lower(),
            timeshift=timeshift,
            filename_format=filename_format
        )

        # assemble with full path
        newfilepath = os.path.sep.join([self.directory, newname])

        self.rename(newfilepath, verbose)




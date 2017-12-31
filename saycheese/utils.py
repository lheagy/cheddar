from exiftool import ExifTool
import datetime


def get_metadata(filepath):
    """
    Get Exchangeable image file format information from an image

    .. code:: python

        filepath = './IMG_001.jpg'
        metadata = get_metadata(filepath)

    """
    with ExifTool() as et:
        metadata = et.get_metadata(filepath)

    return metadata


def filename_by_date(
    image_datetime,
    file_extension="jpg",
    timeshift=None,
    filename_format="%Y-%m-%d %H.%M.%S"
):
    """
    Create a filename for a photo based on the date in the exif. The default
    filename format mimics dropbox.

    .. code::

        filepath = './IMG_001.jpg'
        metadata = get_metadata(filepath)
        newfilename = filename_by_date(metadata)


    A timeshift can be included if you would like to update the time used in
    the filename.

    """

    if timeshift is None:
        timeshift = {"seconds": 0}

    shift = datetime.timedelta(**timeshift)
    image_datetime += shift

    filename = (
        image_datetime.strftime(filename_format) +
        u".{file_extension}".format(file_extension=file_extension)
    )

    return filename


def compute_timeshift(media1, media2, delta=None):
    """
    Compute the timeshift between two images
    """

    if delta is None:
        delta = datetime.timedelta(seconds=0)
    return media2.datetime - media1.datetime + delta


# def merge_libraries(
#     library1,
#     library2,
#     destination="./merged",
#     sync=None,
#     delta=datetime.timedelta(seconds=-1)
# ):

#     if sync is not None:
#         assert type(sync) is list, (
#             "sync must be a list of media objects (one from library1, the "
#             "other from library2)"
#         )



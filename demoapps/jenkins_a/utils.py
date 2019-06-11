import datetime


def stamp_to_datetime(stamp, unit='s', format=None):
    if unit=="ms":
        stamp = int(stamp) / 1000
    d = datetime.datetime.fromtimestamp(stamp)
    if format:
        return d.strftime(format)
    return d
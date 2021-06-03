from os import environ
from dotty_dict import dotty
from app.lang import dictionary


class UnknownLocaleException(Exception): pass


def _(key, local=environ.get('LOCALE', 'en')):
    if local not in dictionary:
        raise UnknownLocaleException
    return dotty(dictionary[local]).get(key, '')
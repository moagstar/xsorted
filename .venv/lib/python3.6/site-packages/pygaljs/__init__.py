__version__ = "1.0.1"

import os


def path(*parts):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), 'static', *parts))


def uri(*parts):
    return "file://%s" % path(*parts)


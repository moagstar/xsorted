#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     fibonacci = xsorted.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

# future
from __future__ import division, print_function, absolute_import
# std
import logging
import contextlib
# local
from . _xsorted import DefaultSerializer, _sort_batches, _merge_sort_batches


__author__ = "Daniel Bradburn"
__copyright__ = "Daniel Bradburn"
__license__ = "MIT"


_logger = logging.getLogger(__name__)


class XSorter:
    """
    xsorted factory.

    Create an xsorted function which uses a custom serializer or batch size.
    """

    def __init__(self, batch_size=8192, serializer=None):
        """
        Initialise this instance.

        :param batch_size:
        :param serializer:
        """
        self.serializer = serializer
        self.batch_size = batch_size

    def __call__(self, iterable, key=None, reverse=False):
        """

        :param iterable:
        :param key:
        :param reverse:

        :return:
        """
        with self._enter():
            batch_ids = _sort_batches(self.batch_size, self.serializer.dump, iterable, key, reverse)
            return _merge_sort_batches(self.serializer.load, batch_ids, key, reverse)

    @contextlib.contextmanager
    def _enter(self):
        """
        """
        # allow serializer to not be a context manager.
        if hasattr(self.serializer, '__enter__'):
            with self.serializer:
                yield
        else:
            yield


# default xsorted function
xsorted = XSorter(serializer=DefaultSerializer())


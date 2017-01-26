#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# future
from __future__ import division, print_function, absolute_import
# std
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:                         # pragma: no cover
    __version__ = 'unknown'     # pragma: no cover
import os
import pickle as serializer
import tempfile
import heapq
import contextlib
# 3rd party
from toolz.itertoolz import partition_all


__author__ = "Daniel Bradburn"
__copyright__ = "Daniel Bradburn"
__license__ = "MIT"


def _default_sort_batches(batch_size, dump, iterable, key=None, reverse=False):
    """

    :param batch_size:
    :param dump:
    :param iterable:
    :param key:
    :param reverse:

    :return:
    """
    batch_ids = []
    for batch in partition_all(batch_size, iterable):
        sorted_batch = sorted(batch, key=key, reverse=reverse)
        batch_id = dump(sorted_batch)
        batch_ids.append(batch_id)
    return batch_ids


def _default_merge_sort_batches(load, batch_ids, key, reverse):
    """

    :param load:
    :param batch_ids:
    :param key:
    :param reverse:

    :return:
    """
    if batch_ids:
        items = map(load, batch_ids)
        return heapq.merge(*items, key=key, reverse=reverse)
    else:
        return []


class XSorter:
    """
    Create an xsorted function which uses a custom serializer or batch size.
    """

    def __init__(self, batch_size=8192, serializer=None,
                 sort_batches=_default_sort_batches,
                 merge_sort_batches=_default_merge_sort_batches):
        """
        Initialise an xsorted function.

        The custom serializer object should expose two functions:

        ``dump(batch)`` - serialize a batch of items to external store, returning a unique id which
                          can be used to reload this batch.
        ``load(batch_id)`` - load a batch from an external source.

        The serializer will be wrapped in a ``with`` statement during invocation if serializer
        object is a context manager.

        :param batch_size: The number of items to sort in each batch.
        :param serializer: Custom serializer object.
        :param sort_batches: Callable which will sort batches individually.
        :param merge_sort_batches: Callable which will merge sort individually sorted batches.
        """
        self.serializer = serializer
        self.sort_batches = lambda *args: sort_batches(batch_size, serializer.dump, *args)
        self.merge_sort_batches = lambda *args: merge_sort_batches(serializer.load, *args)

    def __call__(self, iterable, key=None, reverse=False):
        """
        Return a new sorted iterable from the items in iterable.

        The function is similar to the built-in ``sorted`` function but uses external sorting for
        sorting large data sets that typically don't fit in memory.

        Has two optional arguments which must be specified as keyword arguments.

        :param iterable: The iterable to be sorted.
        :param key: Specifies a function of one argument that is used to extract a comparison key from
                    each list element: ``key=str.lower``. The default value is None (compare the
                    elements directly).
        :param reverse: If set to ``True``, then the list elements are sorted as if each comparison
                        were reversed.

        :return: an iterable which returns the elements of the input iterable in sorted order.
        """
        with self._enter():
            batch_ids = self.sort_batches(iterable, key, reverse)
            return self.merge_sort_batches(batch_ids, key, reverse)

    @contextlib.contextmanager
    def _enter(self):
        """
        Possibly wrap the serializer in ``with`` if the serializer has an ``__enter__`` attribute.
        """
        # allow serializer to not be a context manager.
        if hasattr(self.serializer, '__enter__'):
            with self.serializer:
                yield
        else:
            yield


class DefaultSerializer():
    """
    Default serializer which uses temp files to store sorted batches.
    """
    def __init__(self):
        self.batch_ids = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for batch_id in self.batch_ids:
            if os.path.exists(batch_id):
                os.unlink(batch_id)

    def dump(self, batch):
        """
        Dump the batch to disk.

        :param batch: The batch to dump

        :return: Unique identifier for loading this batch.
        """
        with tempfile.NamedTemporaryFile(delete=False) as fileobj:
            serializer.dump(batch, fileobj)
            self.batch_ids.append(fileobj.name)
            return fileobj.name

    def load(self, batch_id):
        """
        Load a batch from disk.

        :param batch_id: Unique batch id to load.

        :return: The loaded batch.
        """
        with open(batch_id, 'rb') as fileobj:
            return serializer.load(fileobj)


# default xsorted, uses temp files for serialization and a batch size of 8192
_xsorted = XSorter(serializer=DefaultSerializer())


def xsorted(iterable, key=None, reverse=False):
    """
    Return a new sorted iterable from the items in iterable.

    The function is similar to the built-in ``sorted`` function but uses external sorting for
    sorting large data sets that typically don't fit in memory.

    Has two optional arguments which must be specified as keyword arguments.

    :param iterable: The iterable to be sorted.
    :param key: Specifies a function of one argument that is used to extract a comparison key from
                each list element: ``key=str.lower``. The default value is None (compare the
                elements directly).
    :param reverse: If set to ``True``, then the list elements are sorted as if each comparison
                    were reversed.

    :return: an iterable which returns the elements of the input iterable in sorted order.
    """
    return _xsorted(iterable, key, reverse)

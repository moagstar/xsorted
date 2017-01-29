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
import pickle
import tempfile
from contextlib import contextmanager
from functools import partial
# compat
from xsorted.backports_heapq_merge import merge
# 3rd party
from toolz.functoolz import compose
from toolz.itertoolz import partition_all


__author__ = __copyright__ = "Daniel Bradburn"
__license__ = "MIT"


@contextmanager
def serializer():
    """
    Default serializer factory which uses pickle to serialize partitions

    :return: tuple of dump, load, where:

                dump -- a callable taking one parameter which is the iterable to serialize, the
                        function should return an id which can be used to reload the serialized
                        iterable.

                load -- a callable taking an id, the function should return an iterable or
                        generator which iterates the serialized iterable. It is important that
                        this function does not materialize the iterable.
    """
    partition_ids = []

    def dump(partition):
        with tempfile.NamedTemporaryFile(delete=False) as fileobj:
            pickle.dump(partition, fileobj)
            partition_ids.append(fileobj.name)
            return fileobj.name

    def load(partition_id):
        with open(partition_id, 'rb') as fileobj:
            return pickle.load(fileobj)  # todo : need to use streaming

    try:
        yield dump, load
    finally:
        for partition_id in filter(os.path.exists, partition_ids):
            os.unlink(partition_id)


def _split(dump, partition_size, iterable, key=None, reverse=False):
    """
    Spit iterable into a number of sorted partitions of size partition_size (the last partition
    may have fewer items) and serialize using the dump callable.

    :param dump:            Callable which takes an iterable and serializes to some external
                            source, returning an iterable of ids which can be used to reload the
                            externalized partitions.
    :param partition_size:  The number of items to place in each partition.
    :param iterable:        The iterable to split into sorted partitions.
    :param key:             Callable which is used to retrieve the field to sort by.
    :param reverse:         If set to ``True``, then the list elements are sorted as if each
                            comparison were reversed.

    :return: iterable of the ids which can be used to reload the externalized partitions.
    """
    sorted_bound = partial(sorted, key=key, reverse=reverse)
    partitioned = partition_all(partition_size, iterable)
    dump_sorted = compose(dump, sorted_bound)
    return map(dump_sorted, partitioned)


def _merge(load, partition_ids, key=None, reverse=False):
    """
    Merge and sort externalized partitions.

    :param load:          Callable which loads and returns an iterable for iterating the
                          externalized partitions.
    :param partition_ids: Ids which can be used to reload the serialized partitions.
    :param key:           ``sorted`` key parameter.
    :param reverse:       ``sorted`` reverse parameter.

    :return: iterable of merged partitions.
    """
    return merge(*map(load, partition_ids), key=key, reverse=reverse)


def _xsorted(partition_size, serializer_factory, split, merge, iterable, key=None, reverse=False):
    """
    xsorted implementation where dependencies should be injected, athough it is possible to use
    this function directly the xsorter function should be used to pre-bind the dependencies for
    convenience.

    :param partition_size:     The number of items to serialize in each partition.
    :param serializer_factory: Callable returning a context manager which returns a tuple of
                               (dump, load) on ``__enter__``.
    :param split:              Callable which is used to sort and split the given iterable into
                               partitions.
    :param merge:              Callable which is used to merge and sort serialized partitions.
    :param iterable:           The iterable to be sorted.

    :param key:                Specifies a function of one argument that is used to extract a
                               comparison key from each list element: ``key=str.lower``. The
                               default value is None (compare the elements directly).

    :param reverse:            If set to ``True``, then the list elements are sorted as if each
                               comparison were reversed.

    :return: an iterable which returns the elements of the input iterable in sorted order.
    """
    with serializer_factory() as (dump, load):
        partition_ids = split(dump, partition_size, iterable, key, reverse)
        return merge(load, partition_ids, key, reverse)


def xsorter(partition_size=8192, serializer_factory=serializer, split=_split, merge=_merge):
    """
    Generate an xsorted function using the specified partition size, serializer factory, splitter
    and merger.

    :param partition_size:     The number of items to serialize in each partition.
    :param serializer_factory: Context manager which should return a tuple dump and load for
                               serializing data.

                                dump -- a callable taking one parameter which is the iterable to
                                        serialize, the function should return an id which can be
                                        used to reload the serialized iterable.

                                load -- a callable taking an id, the function should return an
                                        iterable or generator which iterates the serialized
                                        iterable. It is important that this function does not
                                        materialize the iterable, otherwise the whole data set will
                                        be loaded in memory, which defeats the object of this kind
                                        of sorting.

    :param split:              Callable which is used to sort and split the given iterable into
                               partitions.
    :param merge:              Callable which is used to merge and sort serialized partitions.

    :return: xsorted function.
    """
    return partial(_xsorted, partition_size, serializer_factory, split, merge)


def xsorted(iterable, key=None, reverse=False):
    """
    Return a new sorted iterable from the items in iterable.

    The function is similar to the built-in ``sorted`` function but uses external sorting for
    sorting large data sets that typically don't fit in memory.

    Has two optional arguments which must be specified as keyword arguments.

    :param iterable: The iterable to be sorted.

    :param key:      Specifies a function of one argument that is used to extract a comparison key
                     from each list element: ``key=str.lower``. The default value is None (compare
                     the elements directly).

    :param reverse:  If set to ``True``, then the list elements are sorted as if each comparison
                     were reversed.

    :return: an iterable which returns the elements of the input iterable in sorted order.
    """
    return xsorter()(iterable, key, reverse)

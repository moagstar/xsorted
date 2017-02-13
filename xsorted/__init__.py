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
import sys
import pickle
import tempfile
from functools import partial
# compat
from contextlib2 import suppress, contextmanager
if sys.version_info[:2] >= (3, 5):
    from heapq import merge
else:
    from xsorted.backports_heapq_merge import merge
# 3rd party
from toolz.functoolz import compose
from toolz.itertoolz import partition_all


__author__ = __copyright__ = "Daniel Bradburn"
__license__ = "MIT"


def _dump(partition):
    """
    Dump the given partition to an external source.

    The default implementation is to pickle the list of objects to a temporary file.

    :param partition: The partition of objects to dump.

    :return: Unique id which can be used to reload the serialized partition. In the case of the
             default implementation this is the path to the temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False) as fileobj:
        for item in partition:
            pickle.dump(item, fileobj)
        return fileobj.name


def _load(partition_id):
    """
    Load a partition from an external source.

    The default implementation yields items loaded and unpickled from a temporary file. After all
    items have been loaded the temporary file is removed.

    :param partition_id: Unique identifier which can be used to reload the partition. In the case
                         of the default implemenation this is the path to the temporary file to
                         load.

    :return: iterable which is loaded from the external source using partition_id.
    """
    if os.path.exists(partition_id):
        try:
            with suppress(EOFError), open(partition_id, 'rb') as fileobj:
                while True:
                    yield pickle.load(fileobj)
        finally:
            os.unlink(partition_id)
    else:
        raise StopIteration()


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
    sort_by_key_and_maybe_reverse = partial(sorted, key=key, reverse=reverse)
    partitioned = partition_all(partition_size, iterable)
    dump_sorted = compose(dump, sort_by_key_and_maybe_reverse)
    return [dump_sorted(x) for x in partitioned]


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


def _xsorted(partition_size, dump, load, split, merge, iterable, key=None, reverse=False):
    """
    xsorted implementation where dependencies should be injected, athough it is possible to use
    this function directly the xsorter function should be used to pre-bind the dependencies for
    convenience.

    :param partition_size:     The number of items to serialize in each partition.

    :param dump:               Callable taking one parameter which is the iterable to
                               serialize, the function should return an id which can be
                               used to reload the serialized iterable.

    :param load:               Callable taking an id, the function should return an
                               iterable or generator which iterates the serialized
                               iterable. It is important that this function does not
                               materialize the iterable, otherwise the whole data set will
                               be loaded in memory, which defeats the object of this kind
                               of sorting.

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
    partition_ids = split(dump, partition_size, iterable, key, reverse)
    return merge(load, partition_ids, key, reverse)


def xsorter(partition_size=8192, dump=_dump, load=_load, split=_split, merge=_merge):
    """
    Generate an xsorted function using the specified partition size, serializer factory, splitter
    and merger.

    :param partition_size:     The number of items to serialize in each partition.

    :param dump:               Callable taking one parameter which is the iterable to
                               serialize, the function should return an id which can be
                               used to reload the serialized iterable.

    :param load:               Callable taking an id, the function should return an
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
    return partial(_xsorted, partition_size, dump, load, split, merge)


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

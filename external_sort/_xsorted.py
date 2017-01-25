# future
from __future__ import division, print_function, absolute_import
# std
import os
import pickle as serializer
import contextlib
import tempfile
import heapq
# 3rd party
from toolz.itertoolz import partition_all


@contextlib.contextmanager
def _default_dump_load():
    """

    :return:
    """

    batch_ids = []

    def default_dump(batch):
        with tempfile.NamedTemporaryFile(delete=False) as fileobj:
            serializer.dump(batch, fileobj)
            batch_ids.append(fileobj.name)
            return fileobj.name

    def default_load(batch_id):
        with open(batch_id) as fileobj:
            return serializer.load(fileobj)

    try:
        yield default_dump, default_load
    finally:
        for batch_id in batch_ids:
            os.unlink(batch_id)


def _sort_batches(sorter, iterable, key, reverse):
    """

    :param iterable:
    :param key:
    :param reverse:

    :return:
    """
    batch_ids = []
    for batch in partition_all(sorter.batch_size, iterable):
        sorted_batch = sorted(batch, key=key, reverse=reverse)
        batch_id = sorter.dump(sorted_batch)
        batch_ids.append(batch_id)
    return batch_ids


def _merge_sort_batches(sorter, batch_ids, key, reverse):
    """

    :param batch_ids:
    :param key:
    :param reverse:

    :return:
    """
    if batch_ids:
        items = map(sorter.load, batch_ids)
        return heapq.merge(*items, key=key, reverse=reverse)
    else:
        return []

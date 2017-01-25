# future
from __future__ import division, print_function, absolute_import
# std
import os
import pickle as serializer
import tempfile
import heapq
# 3rd party
from toolz.itertoolz import partition_all


class DefaultSerializer():
    """
    """

    def __init__(self):
        """

        """
        self.batch_ids = []

    def __enter__(self):
        """

        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        for batch_id in self.batch_ids:
            if os.path.exists(batch_id):
                os.unlink(batch_id)

    def dump(self, batch):
        """

        :param batch:
        :return:
        """
        with tempfile.NamedTemporaryFile(delete=False) as fileobj:
            serializer.dump(batch, fileobj)
            self.batch_ids.append(fileobj.name)
            return fileobj.name

    def load(self, batch_id):
        """

        :param batch_id:
        :return:
        """
        with open(batch_id, 'rb') as fileobj:
            return serializer.load(fileobj)


def _sort_batches(batch_size, dump, iterable, key, reverse):
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


def _merge_sort_batches(load, batch_ids, key, reverse):
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

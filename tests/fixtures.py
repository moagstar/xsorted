# std
import uuid
import random
# 3rd party
import pytest
# local
from xsorted import xsorter


class CustomSerializer:
    """
    Custom serializer using a simple in-memory dict.
    """
    def __init__(self):
        self.store = {}

    def dump(self, thing):
        object_id = uuid.uuid4()
        self.store[object_id] = thing
        return object_id

    def load(self, object_id):
        return self.store[object_id]


@pytest.fixture()
def xsorted_custom_serializer_fixture():
    """
    Fixture for creating an xsorted function with an instance of CustomSerializer as serializer.
    """
    serializer = CustomSerializer()
    return xsorter(dump=serializer.dump, load=serializer.load)


@pytest.fixture()
def benchmark_items_fixture():
    """
    Fixture for creating a list of items for sorting which can be used for benchmarking.
    """
    items = list(range(pow(10, 6)))
    random.seed(0)
    random.shuffle(items)
    return items

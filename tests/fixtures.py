# std
import uuid
import random
# compat
import mock
# 3rd party
import pytest
# local
from xsorted import serializer, xsorter


@pytest.fixture()
def serializer_fixture():
    """
    Default serializer fixture, the serializer is not entered via ``with``.
    """
    return serializer()


@pytest.yield_fixture()
def serializer_yield_fixture():
    """
    Default serializer fixture, the serializer is already entered via ``with``.
    """
    with serializer() as (dump, load):
        yield dump, load


class CustomSerializer:
    """
    Custom serializer using an in-memory store.
    """
    def __init__(self):
        self.store = {}

    def __enter__(self):
        return self.dump, self.load

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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
    return xsorter(serializer_factory=CustomSerializer)


@pytest.fixture()
def xsorted_custom_serializer_context_manager_fixture():
    """
    Fixture for creating an xsorted function with an instance of CustomSerializerContextManager
    as serializer.
    """
    return xsorter(serializer_factory=CustomSerializerContextManager)


@pytest.fixture()
def benchmark_items():
    """
    Fixture for creating a list of items for sorting which can be used for benchmarking.
    """
    items = list(range(pow(10, 6)))
    random.seed(0)
    random.shuffle(items)
    return items

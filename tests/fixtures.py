# std
import uuid
import random
# 3rd party
import pytest
# local
from xsorted import DefaultSerializer, XSorter


@pytest.fixture()
def default_serializer_fixture():
    """
    Fixture for creating a DefaultSerializer.
    """
    return DefaultSerializer()


class CustomSerializer:
    """
    Custom serializer using an in-memory store.
    """
    def __init__(self):
        self.store = {}

    def dump(self, thing):
        object_id = uuid.uuid4()
        self.store[object_id] = thing
        return object_id

    def load(self, object_id):
        return self.store[object_id]


class CustomSerializerContextManager(CustomSerializer):
    """
    Custom serializer using an in-memory store, that can be used as a context manager.
    """
    def __init__(self):
        super(CustomSerializerContextManager, self).__init__()
        self.enter_called = False
        self.exit_called = False

    def __enter__(self):
        self.enter_called = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_called = True


@pytest.fixture()
def xsorted_custom_serializer_fixture():
    """
    Fixture for creating an xsorted function with an instance of CustomSerializer as serializer.
    """
    return XSorter(serializer=CustomSerializer())


@pytest.fixture()
def xsorted_custom_serializer_context_manager_fixture():
    """
    Fixture for creating an xsorted function with an instance of CustomSerializerContextManager
    as serializer.
    """
    return XSorter(serializer=CustomSerializerContextManager())


@pytest.fixture()
def benchmark_items():
    """
    Fixture for creating a list of items for sorting which can be used for benchmarking.
    """
    items = list(range(pow(10, 6)))
    random.seed(0)
    random.shuffle(items)
    return items

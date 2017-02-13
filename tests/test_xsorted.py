#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
import os
import random
# 3rd party
import pytest
from mock import Mock
from hypothesis import given, example, strategies as st
from toolz.itertoolz import partition_all
# local
from xsorted import xsorted, _split, _merge, _dump, _load
from . fixtures import xsorted_custom_serializer_fixture, benchmark_items_fixture


def assert_property_xsorted_is_the_same_as_sorted(_xsorted, things, reverse):
    """
    Verify the property that given a list of things, when the list of things is sorted using
    ``xsorted``, the result should be the same as when the list of things is sorted using the
    builtin ``sorted``.

    :param _xsorted: Xsorted function under test.
    :param things: Iterable containing the list of things to sort.
    :param reverse: True if things should be sorted in reverse order.
    """
    expected = list(sorted(things, reverse=reverse))
    actual = list(_xsorted(things, reverse=reverse))
    assert actual == expected


@given(things=st.lists(st.integers()), reverse=st.booleans())
@example(things=[0, 0], reverse=True)
def test_property_xsorted_is_the_same_as_sorted(things, reverse):
    """
    Verify the property that xsorted == sorted.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted, things, reverse)


@given(lists_of_things=st.lists(st.lists(st.integers())))
def test_serializer_dump_load(lists_of_things):
    """
    Verify that the default serializer loads as expected.
    """
    ids = [_dump(thing) for thing in lists_of_things]
    actual = [list(_load(id)) for id in ids]
    assert lists_of_things == actual


def test_default_serializer_cleanup():
    """
    Verify that the default serializer cleans up after itself.
    """
    path = _dump([0])
    assert os.path.exists(path)
    list(_load(path))
    assert not os.path.exists(path)


@given(things=st.lists(st.integers()), reverse=st.booleans())
def test_property_xsorted_custom_serializer_is_the_same_as_sorted(xsorted_custom_serializer_fixture,
                                                                  things, reverse):
    """
    Verify that we can supply custom serialization dump and load.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted_custom_serializer_fixture, things, reverse)


@pytest.mark.xfail()
def test_property_xsorted_custom_merge_is_the_same_as_sorted():
    """
    Verify that we can supply custom merge function.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_property_xsorted_custom_split_is_the_same_as_sorted():
    """
    Verify that we can supply custom split function.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_property_xsorted_combined_custom_impl_is_the_same_as_sorted():
    """
    Verify the combination of custom implementation details.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_is_external():
    """
    Verify that when sorting a large iterable that not all items are loaded in memory.
    """
    assert 0, 'not implemented'


@given(st.integers(min_value=1, max_value=1000), st.integers(min_value=1, max_value=1000))
def test_split(range_size, partition_size):
    """
    Verify that the default _split correctly splits the iterable into sorted batches.
    """
    dump = Mock()

    iterable = list(range(range_size))

    list(_split(partition_size=partition_size, dump=dump, iterable=iterable))
    expected_call_count = (range_size // partition_size) + int(bool(range_size % partition_size))

    assert dump.call_count == expected_call_count


@given(
    partition_size=st.integers(min_value=1, max_value=100),
    num_items=st.integers(min_value=0, max_value=100),
)
def test_merge(partition_size, num_items):
    """
    Verify that _merge correctly merges batches into one sorted iterable.
    """
    items = range(num_items)
    partitions = list(partition_all(partition_size, items))
    partition_ids = range(len(partitions))
    random.shuffle(partitions)
    merged = _merge(lambda x: partitions[x], partition_ids)
    assert list(merged) == list(items)


def test_benchmark_xsorted(benchmark, benchmark_items_fixture):
    """
    Benchmark the performance of the ``xsorted`` function.
    """
    benchmark(lambda: xsorted(benchmark_items_fixture))


def test_benchmark_sorted(benchmark, benchmark_items_fixture):
    """
    Benchmark the performance of the built-in ``sorted`` function for comparing with ``xsorted``.
    """
    benchmark(lambda: sorted(benchmark_items_fixture))

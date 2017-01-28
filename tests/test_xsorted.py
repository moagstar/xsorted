#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
import os
# 3rd party
import pytest
from mock import patch, Mock
from hypothesis import given, settings
import hypothesis.strategies as st
# local
from xsorted import xsorted, _split, _merge
from fixtures import (
    serializer_fixture,
    serializer_yield_fixture,
    xsorted_custom_serializer_fixture,
    benchmark_items,
)


def assert_property_xsorted_is_the_same_as_sorted(_xsorted, things, reverse):
    """
    Verify the property that given a list of things, when the list of things is sorted using
    ``xsorted``, the result should be the same as when the list of things is sorted using the
    builtin ``sorted``.

    :param iterable: Iterable containing the list of things to sort.
    """
    expected = list(sorted(things, reverse=reverse))
    actual = list(_xsorted(things, reverse=reverse))
    assert actual == expected


@given(things=st.lists(st.integers()), reverse=st.booleans())
def test_property_xsorted_is_the_same_as_sorted(things, reverse):
    """
    Verify that the default xsorted sorts as expected.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted, things, reverse)


@given(things=st.lists(st.integers()))
def test_serializer_dump_load(serializer_yield_fixture, things):
    """
    Verify that the default serializer loads as expected.
    """
    dump, load = serializer_yield_fixture
    ids = [dump(thing) for thing in things]
    actual = [load(id) for id in ids]
    assert things == actual


def test_default_serializer_cleanup(serializer_fixture):
    """
    Verify that the default serializer cleans up after itself.
    """
    with serializer_fixture as (dump, load):
        path = dump(0)
        assert os.path.exists(path)
    assert not os.path.exists(path)


@given(things=st.lists(st.integers()), reverse=st.booleans())
def test_custom_serializer_context_manager(xsorted_custom_serializer_fixture, things, reverse):
    """
    Verify that we can use a custom serializer that is not a context manager.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted_custom_serializer_fixture, things, reverse)


def test_split():
    """
    Verify that sort_batches splits the iterable into sorted batches.
    """
    dump = Mock()

    range_size, partition_size = 17, 4
    iterable = list(range(range_size))

    list(_split(partition_size=partition_size, dump=dump, iterable=iterable))
    expected_call_count = (range_size // partition_size) + int(bool(range_size % partition_size))

    assert dump.call_count == expected_call_count


@pytest.mark.xfail()
def test_merge():
    """
    Verify that merge_sort_batches merges batches into one sorted iterable.
    """
    assert 0, 'not implemented'


def test_benchmark_xsorted(benchmark, benchmark_items):
    """
    Benchmark the performance of the ``xsorted`` function.
    """
    benchmark(lambda: xsorted(benchmark_items))


def test_benchmark_sorted(benchmark, benchmark_items):
    """
    Benchmark the performance of the built-in ``sorted`` function for comparing with ``xsorted``.
    """
    benchmark(lambda: sorted(benchmark_items))

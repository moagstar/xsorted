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
from xsorted import xsorted, _default_sort_batches, _default_merge_sort_batches
from fixtures import (
    default_serializer_fixture,
    xsorted_custom_serializer_fixture,
    xsorted_custom_serializer_context_manager_fixture,
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
def test_default_serializer_dump_load(default_serializer_fixture, things):
    """
    Verify that the default serializer loads as expected.
    """
    with default_serializer_fixture:
        ids = [default_serializer_fixture.dump(thing) for thing in things]
        actual = [default_serializer_fixture.load(id) for id in ids]
        assert things == actual


def test_default_serializer_cleanup(default_serializer_fixture):
    """
    Verify that the default serializer cleans up after itself.
    """
    with default_serializer_fixture:
        path = default_serializer_fixture.dump(0)
        assert os.path.exists(path)
    assert not os.path.exists(path)


@given(things=st.lists(st.integers()), reverse=st.booleans())
def test_custom_serializer(xsorted_custom_serializer_fixture, things, reverse):
    """
    Verify that we can use a custom serializer that is a context manager.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted_custom_serializer_fixture, things, reverse)


@given(things=st.lists(st.integers()), reverse=st.booleans())
def test_custom_serializer_context_manager(xsorted_custom_serializer_context_manager_fixture, things, reverse):
    """
    Verify that we can use a custom serializer that is not a context manager.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted_custom_serializer_context_manager_fixture, things, reverse)
    assert xsorted_custom_serializer_context_manager_fixture.serializer.enter_called
    assert xsorted_custom_serializer_context_manager_fixture.serializer.exit_called


def test_default_sort_batches():
    """
    Verify that sort_batches splits the iterable into sorted batches.
    """
    dump = Mock()
    range_size, batch_size = 17, 4
    _default_sort_batches(batch_size=batch_size, dump=dump, iterable=range(range_size))
    expected = (range_size // batch_size) + int(bool(range_size % batch_size))
    assert dump.call_count == expected


@pytest.mark.xfail()
def test_merge_sort_batches():
    """
    Verify that merge_sort_batches merges batches into one sorted iterable.
    """
    assert 0, 'not implemented'


def test_benchmark_xsorted(benchmark, benchmark_items):
    benchmark(lambda: xsorted(benchmark_items))


def test_benchmark_sorted(benchmark, benchmark_items):
    benchmark(lambda: sorted(benchmark_items))
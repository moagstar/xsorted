#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
from unittest.mock import patch
# 3rd party
import pytest
from hypothesis import given, settings
import hypothesis.strategies as st
# local
from xsorted.xsorted import xsorted


@st.composite
def lists_of_things(draw):
    item_strategy = draw(st.sampled_from((
        st.integers(),
        st.fractions(),
        st.text(),
        st.lists(st.text())
    )))
    return draw(st.lists(item_strategy))


@given(lists_of_things())
def test_property_xsorted_is_the_same_as_sorted(iterable):
    """
    Verify the property that given a list of things, when the list of things is sorted using
    ``xsorted``, the result should be the same as when the list of things is sorted using the
    builtin ``sorted``.

    :param iterable: Iterable containing the list of things to sort.
    """
    expected = list(sorted(list(iterable)))
    actual = list(xsorted(list(iterable)))
    assert actual == expected


@pytest.mark.xfail()
def test_default_serializer_dump():
    """
    Verify that the default serializer dumps as expected.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_default_serializer_load():
    """
    Verify that the default serializer loads as expected.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_default_serializer_cleanup():
    """
    Verify that the default serializer cleans up after itself.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_custom_serializer_context_manager():
    """
    Verify that we can use a custom serializer that is a context manager.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_custom_serializer_no_context_manager():
    """
    Verify that we can use a custom serializer that is not a context manager.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_sort_batches():
    """
    Verify that sort_batches splits the iterable into sorted batches.
    """
    assert 0, 'not implemented'


@pytest.mark.xfail()
def test_merge_sort_batches():
    """
    Verify that merge_sort_batches merges batches into one sorted iterable.
    """
    assert 0, 'not implemented'

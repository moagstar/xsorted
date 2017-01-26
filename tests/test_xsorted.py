#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
import os
from unittest.mock import patch
# 3rd party
import pytest
from hypothesis import given, settings
import hypothesis.strategies as st
# local
from xsorted import xsorted
from fixtures import (
    default_serializer_fixture,
    xsorted_custom_serializer_fixture,
    xsorted_custom_serializer_context_manager_fixture,
)


@st.composite
def lists_of_things(draw):
    item_strategy = draw(st.sampled_from((
        st.integers(),
        st.fractions(),
        st.text(),
        st.lists(st.text())
    )))
    return draw(st.lists(item_strategy))


def assert_property_xsorted_is_the_same_as_sorted(_xsorted, things):
    """
    Verify the property that given a list of things, when the list of things is sorted using
    ``xsorted``, the result should be the same as when the list of things is sorted using the
    builtin ``sorted``.

    :param iterable: Iterable containing the list of things to sort.
    """
    expected = list(sorted(things))
    actual = list(_xsorted(things))
    assert actual == expected


@given(lists_of_things())
def test_property_xsorted_is_the_same_as_sorted(things):
    """
    Verify that the default xsorted sorts as expected.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted, things)


@given(things=lists_of_things())
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


@given(things=lists_of_things())
def test_custom_serializer(xsorted_custom_serializer_fixture, things):
    """
    Verify that we can use a custom serializer that is a context manager.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted_custom_serializer_fixture, things)


@given(things=lists_of_things())
def test_custom_serializer_context_manager(xsorted_custom_serializer_context_manager_fixture, things):
    """
    Verify that we can use a custom serializer that is not a context manager.
    """
    assert_property_xsorted_is_the_same_as_sorted(xsorted_custom_serializer_context_manager_fixture, things)
    assert xsorted_custom_serializer_context_manager_fixture.serializer.enter_called
    assert xsorted_custom_serializer_context_manager_fixture.serializer.exit_called


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

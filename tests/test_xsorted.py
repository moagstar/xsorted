#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
from unittest.mock import patch
# 3rd party
from hypothesis import given, settings
import hypothesis.strategies as st
# local
from external_sort.xsorted import xsorted


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
@settings(max_examples=5000)
def test_property_xsorted_is_the_same_as_sorted(iterable):
    expected = list(sorted(list(iterable)))
    actual = list(xsorted(list(iterable)))
    assert actual == expected


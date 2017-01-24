#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
# 3rd party
import pytest
from hypothesis import given
import hypothesis.strategies as st
# local
from external_sort.xsorted import xsorted


@given(st.lists(st.text()))
def test_xsorted(iterable):
    expected = list(sorted(list(iterable)))
    actual = list(xsorted(list(iterable)))
    assert actual == expected

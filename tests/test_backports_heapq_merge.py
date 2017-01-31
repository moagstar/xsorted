# std
import collections
# 3rd party
from hypothesis import strategies as st, given
from xsorted.backports_heapq_merge import merge


def _iterables(iterables, random, reverse, key):
    iterables = [sorted(x, key=key, reverse=reverse) for x in iterables]
    random.shuffle(iterables)
    return iterables


def _expected(iterables, reverse, key):
    flattened = (y for x in iterables for y in x)
    expected = list(sorted(flattened, key=key, reverse=reverse))
    return expected


def _actual(iterables, reverse, key):
    merged = merge(*iterables, key=key, reverse=reverse)
    return list(merged)


def _do_test(iterables, random, reverse, key=None):
    iterables = _iterables(iterables, random, reverse, key)
    assert _expected(iterables, reverse, key) == _actual(iterables, reverse, key)


@given(
    iterables=st.lists(st.lists(st.integers())),
    random=st.randoms(),
    reverse=st.booleans(),
)
def test_heapq_merge(iterables, random, reverse):
    _do_test(iterables, random, reverse)


point_fields = 'x', 'y', 'z'
Point = collections.namedtuple('Point', point_fields)


@st.composite
def points(draw):
    return Point(*(draw(st.integers()) for _ in range(3)))


@given(
    iterables=st.lists(st.lists(points())),
    random=st.randoms(),
    reverse=st.booleans(),
    attr=st.sampled_from(point_fields),
)
def test_heapq_merge_custom_key(iterables, random, reverse, attr):
    _do_test(iterables, random, reverse, lambda p: getattr(p, attr))

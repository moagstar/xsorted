# 3rd party
from hypothesis import strategies as st, given
from xsorted.backports_heapq_merge import merge


@given(
    iterables=st.lists(st.lists(st.integers())),
    random=st.randoms(),
    reverse=st.booleans(),
)
def test_heapq_merge(iterables, random, reverse):
    iterables = [sorted(x, reverse=reverse) for x in iterables]
    random.shuffle(iterables)
    expected = list(sorted(y for x in iterables for y in x))
    if reverse:
        expected = list(reversed(expected))
    actual = list(merge(*iterables, reverse=reverse))
    assert expected == actual

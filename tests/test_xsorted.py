#!/usr/bin/env python
# -*- coding: utf-8 -*-


# std
import os
import random
import threading
import time
import collections
# 3rd party
import pygal
from pygal.style import CleanStyle as memory_profile_chart_style
import psutil
import pytest
from mock import Mock
from hypothesis import given, example, strategies as st
from toolz.itertoolz import partition_all
# local
from xsorted import xsorter, xsorted, _split, _merge, _dump, _load
from . fixtures import xsorted_custom_serializer_fixture, benchmark_items_fixture
from . util import random_strings


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


@given(things=st.lists(st.integers(min_value=-2147483648, max_value=4294967295)), reverse=st.booleans())
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


def do_benchmark(items, function_to_test, benchmark=None):
    """
    Generic benchmarking function that will iterate through the ``items`` sorted using ``function_under_test``.

    :param items: The items to sort.
    :param function_to_test: The sort function to use.
    :param benchmark: Benchmark fixture if this should be run as part of pytest-benchmark
    """
    def do():
        for _ in function_to_test(items):
            pass
    if benchmark is None:
        do()
    else:
        benchmark(do)


def export_memory_profile_chart(memory_usage_samples, num_strings, strings_length):
    """
    Export an svg chart of a memory profile run.

    :param memory_usage_samples: List of tuples (elapsed time, memory usage) sampled during profiling.
    :param num_strings: The number of strings that were generated.
    :param strings_length: The length of the strings generated.

    :return: Path to the generated svg file
    """
    strings_size_kb = int(strings_length / 1000)
    # TODO : Would be nice to some more info about the environment used for the run, version, processor, memory etc.
    chart = pygal.XY(
        title='Memory Used to Generate and Sort {num_strings} Random {strings_size_kb}KB Strings'.format(**locals()),
        fill=True,
        range=(0, num_strings * 1.1),
        show_dots=False,
        x_title='Time (seconds)',
        y_title='Memory Usage (KB)',
        style=memory_profile_chart_style,
    )

    for function_under_test, memory_usage in memory_usage_samples.items():
        chart.add(function_under_test, memory_usage)

    path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'test_profile_memory.svg')
    chart.render_to_file(path)

    return path


def test_profile_memory():
    """
    Profile the memory used when sorting a large memory object using ``xsorted`` compared to ``sorted``.

    The sorting is performed in a separate thread, and in the main thread the memory usage is sampled. The difference
    between the process memory usage at the start of the test and the memory usage at the sample point are recorded.
    We expect sorted to use more memory than xsorted. If this is not the case then xsorted is most likely not a
    correct external ort.
    """
    process = psutil.Process()

    num_strings, strings_length = int(1e5 / 2), 1000
    memory_usage_samples = collections.defaultdict(list)

    for function_under_test in (sorted, xsorted):

        strings = random_strings(length=strings_length, num=num_strings)
        thread = threading.Thread(target=do_benchmark, args=(strings, function_under_test))

        thread.start()
        start_time = time.clock()
        start = process.memory_info_ex().rss

        while thread.is_alive():
            thread.join(0.001)
            value = (process.memory_info_ex().rss - start) / 1e3
            point = time.clock() - start_time, value
            memory_usage_samples[function_under_test.__name__].append(point)

    export_memory_profile_chart(memory_usage_samples, num_strings, strings_length)

    # extract only the memory usage from the sorted dict for determining the peak usage for each function under test.
    values_only = (
        (sample[1] for sample in samples[1])
        for samples in sorted(memory_usage_samples.items())
    )
    peak_sorted, peak_xsorted = map(max, values_only)
    assert peak_sorted / peak_xsorted >= 15


@pytest.mark.parametrize('partition_size', [
    1024,
    # 2048,
    # 4096,
    # 8192,
])
def test_benchmark_xsorted(partition_size, benchmark, benchmark_items_fixture):
    """
    Benchmark the performance of the ``sorted`` function (for comparison)
    """
    xsorted_ = xsorter(partition_size=partition_size)
    do_benchmark(benchmark_items_fixture, xsorted_, benchmark)


def test_benchmark_sorted(benchmark, benchmark_items_fixture):
    """
    Benchmark the performance of the ``sorted`` function (for comparison)
    """
    do_benchmark(benchmark_items_fixture, sorted, benchmark)


@pytest.mark.skip()
def test_benchmark_xsorted_debug(benchmark_items_fixture):
    """
    Debug the benchmark test of the performance of the ``xsorted`` function since both benchmarking and debugging use
    settrace. Just comment out the skip mark when debugging.
    """
    do_benchmark(benchmark_items_fixture, xsorted)

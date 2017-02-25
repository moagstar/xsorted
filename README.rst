.. image:: https://travis-ci.org/moagstar/xsorted.svg?branch=master
    :target: https://travis-ci.org/moagstar/xsorted
    
.. image:: https://coveralls.io/repos/github/moagstar/xsorted/badge.svg?branch=master
    :target: https://coveralls.io/github/moagstar/xsorted?branch=master


=======
xsorted
=======

Like ``sorted`` but using external sorting so that large data sets can be sorted, for example:

>>> from random import random
>>> from six.moves import xrange
>>> from xsorted import xsorted
>>> for x in xsorted(random() for _ in xrange(int(1e7))): pass

The only restriction is that the items must be pickleable (or you can provide your own serializer for externalizing
partitions of items).

Motivation
----------

It is sometimes necessary to sort a dataset without having to load the entire set into memory. For example, if you
want to group a very large csv file by one of it's columns. There are several ways in which this can be achieved, a
common solution is to use the unix command ``sort``. However unix ``sort`` does not offer the flexibility of the python
csv module. Instead of writing a specific csv external sort I implemented ``xsorted``, which attempts to generalize
external sorting of any python iterable in a similar way in which ``sorted`` generalises the sorting of any iterable.

Installation
------------

``$ pip install xsorted``

Usage
-----

Just like ``sorted``...

>>> from xsorted import xsorted
>>> ''.join(xsorted('qwertyuiopasdfghjklzxcvbnm'))
'abcdefghijklmnopqrstuvwxyz'

With ``reverse``...

>>> ''.join(xsorted('qwertyuiopasdfghjklzxcvbnm', reverse=True))
'zyxwvutsrqponmlkjihgfedcba'

And a custom ``key``...

>>> list(xsorted(('qwerty', 'uiop', 'asdfg', 'hjkl', 'zxcv', 'bnm'), key=lambda x: x[1]))
['uiop', 'hjkl', 'bnm', 'asdfg', 'qwerty', 'zxcv']

The implementation details of ``xsorted`` can be customized using the factory ``xsorter`` (in order to provide
the same interface as ``sorted`` the partition_size is treated as an implementation detail):

>>> from xsorted import xsorter
>>> xsorted_custom = xsorter(partition_size=4)
>>> ''.join(xsorted_custom('qwertyuiopasdfghjklzxcvbnm'))
'abcdefghijklmnopqrstuvwxyz'

Memory Usage
------------

The main reason to use ``xsorted`` over ``sorted`` is where memory usage is a bigger concern than speed. The following
chart compares the sampled memory usage of ``xsorted`` vs ``sorted`` when sorting 50000 1KB strings. As can be seen the
memory usage when sorting an iterable with ``sorted`` is roughly equivalent to the memory of the data being sorted,
while with ``xsorted`` the memory usage will be proportional to the number of partitions required to perform the
external sort.

.. image:: https://cdn.rawgit.com/moagstar/xsorted/master/docs/test_profile_memory.svg

It should be noted that we cannot read too much into the time difference in this chart. The memory profile test is
performed by running the sorting algorithm in a separate thread, sampling the memory usage in the main thread. Sampling
memory usage in this way however has a detrimental effect on performance, more so for ``sorted`` than ``xsorted``
due to the additional IO required in ``xsorted``. ``multiprocessing`` could be an option in order to reduce the
performance impact, however the main point of the test is to illustrate the difference in memory usage.

The following section presents some more detailed microbenchmarks which show the difference in performance of the two
sorting functions.

Microbenchmarks
---------------

Again 50000 1KB strings are sorted, benchmarked using `pytest-benchmark
<https://pytest-benchmark.readthedocs.io/en/latest//>`_.

**xsorted**

.. image:: https://cdn.rawgit.com/moagstar/xsorted/250fda21/docs/hist-tests_test_xsorted.py_test_benchmark_xsorted%5B1024%5D.svg

**sorted**

.. image:: https://cdn.rawgit.com/moagstar/xsorted/a21804fa/docs/hist-tests_test_xsorted.py_test_benchmark_sorted.svg

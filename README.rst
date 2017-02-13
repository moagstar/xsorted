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
>>> nums = (random() for _ in xrange(pow(10, 7)))
>>> for x in xsorted(nums): pass

The only restriction is that the items must be pickleable.

Motivation
----------

It is sometimes necessary to sort a dataset without having to load the entire set into memory. For example, if you
want to group a very large csv file by one of it's columns. There are several ways in which this can be achieved, a
common solution is to use the unix command ``sort``. However unix ``sort`` does not offer the flexibility of the python
csv module. ``xsorted`` attempts to generalize external sorting of any python iterable (the only restriction is that
the items must be pickleable) in a similar way in which ``sorted`` generalises the sorting of any iterable.

Installation
------------

```$ pip install xsorted```

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

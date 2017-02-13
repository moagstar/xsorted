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


.. image:: https://travis-ci.org/moagstar/xsorted.svg?branch=master
    :target: https://travis-ci.org/moagstar/xsorted

=======
xsorted
=======

Like ``sorted`` but using external sorting so that large data sets can be sorted.

Usage
-----

>>> from xsorted import xsorted
>>> ''.join(xsorted('qwertyuiopasdfghjklzxcvbnm'))
'abcdefghijklmnopqrstuvwxyz'

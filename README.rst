
.. image:: https://travis-ci.org/moagstar/xsorted.svg?branch=master
    :target: https://travis-ci.org/moagstar/xsorted
    
.. image:: https://coveralls.io/repos/github/moagstar/xsorted/badge.svg?branch=master
    :target: https://coveralls.io/github/moagstar/xsorted?branch=master

=======
xsorted
=======

Like ``sorted`` but using external sorting so that large data sets can be sorted.

Usage
-----

>>> from xsorted import xsorted
>>> ''.join(xsorted('qwertyuiopasdfghjklzxcvbnm'))
'abcdefghijklmnopqrstuvwxyz'

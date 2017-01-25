=======
xsorted
=======

Like ``sorted`` but using external sorting so that large data sets can be sorted.

Usage
-----

>>> from xsorted import xsorted
>>> ''.join(xsorted('qwertyuiopasdfghjklzxcvbnm'))
'abcdefghijklmnopqrstuvwxyz'

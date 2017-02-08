from random import random
from six.moves import xrange
from xsorted import xsorted

nums = (random() for _ in xrange(pow(10, 7)))
for x in xsorted(nums):
    pass

# std
import random
import string
# compat
from six.moves import xrange


def random_strings(num, length, seed=0):
    random.seed(seed)
    return (''.join([random.choice(string.printable)] * length) for _ in xrange(num))
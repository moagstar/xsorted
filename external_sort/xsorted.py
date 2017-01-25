#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
     fibonacci = external_sort.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

# future
from __future__ import division, print_function, absolute_import
# std
import sys
import argparse
import logging
import contextlib
# local
from external_sort import __version__
from . _xsorted import DefaultSerializer, _sort_batches, _merge_sort_batches


__author__ = "Daniel Bradburn"
__copyright__ = "Daniel Bradburn"
__license__ = "none"


_logger = logging.getLogger(__name__)


class XSorter:
    """
    """

    def __init__(self, batch_size=8192, serializer=None):
        """

        :param batch_size:
        :param serializer:
        """
        self.serializer = serializer
        self.batch_size = batch_size

    def __call__(self, iterable, key=None, reverse=False):
        """

        :param iterable:
        :param key:
        :param reverse:

        :return:
        """
        with self._enter():
            batch_ids = _sort_batches(self.batch_size, self.serializer.dump, iterable, key, reverse)
            return _merge_sort_batches(self.serializer.load, batch_ids, key, reverse)

    @contextlib.contextmanager
    def _enter(self):
        """
        """
        # allow serializer to not be a context manager.
        if hasattr(self.serializer, '__enter__'):
            with self.serializer:
                yield
        else:
            yield


xsorted = XSorter(serializer=DefaultSerializer())


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonnaci demonstration")
    parser.add_argument(
        '--version',
        action='version',
        version='external_sort {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="n-th Fibonacci number",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

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
import os
import sys
import pickle
import argparse
import logging
import contextlib
import tempfile
import shutil
import heapq
# 3rd party
from toolz.itertoolz import partition_all
# local
from external_sort import __version__


__author__ = "Daniel Bradburn"
__copyright__ = "Daniel Bradburn"
__license__ = "none"


_logger = logging.getLogger(__name__)


batch_size = 8192
temp_root = None


def xsorted(iterable, key=None, reverse=False):
    """


    :param iterable:
    :param key:
    :param reverse:
    :param batch_size:
    :param temp_root:

    :return:
    """
    with _temp_dir(temp_root) as temp_dir_path:

        batches = []
        for batch_id, batch in enumerate(partition_all(batch_size, iterable)):
            path = os.path.join(temp_dir_path, str(batch_id))
            batches.append(path)
            with open(path, 'wb') as fileobj:
                sorted_batch = sorted(batch, key, reverse)
                pickle.dump(sorted_batch, fileobj)

        def load(batch_id):
            path = os.path.join(temp_dir_path, str(batch_id))
            with open(path) as fileobj:
                for item in pickle.load(fileobj):
                    yield item

        items = (item for batch_id in batches for item in load(batch_id))
        return heapq.merge(items, key, reverse)


@contextlib.contextmanager
def _temp_dir(temp_root):
    """
    Context manager which creates a temporary directory on enter, removing the tree on exit.

    :param temp_root: Directory to create the temp directory under.

    """
    temp_dir_path = tempfile.mkdtemp(dir=temp_root)
    try:
        yield temp_dir_path
    finally:
        shutil.rmtree(temp_dir_path, ignore_errors=True)


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

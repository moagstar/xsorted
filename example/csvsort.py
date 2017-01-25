"""
example showing how xsorted can be used to sort csv files.
"""

# std
import os
import sys
import csv
import random
# local
from xsorted import xsorted


if __name__ == '__main__':

    input_path = os.path.join(os.path.dirname(__file__), 'names.csv')
    with open(input_path) as fileobj:
        reader = csv.reader(fileobj)

        headers = next(reader)
        items = list(reader)
        random.shuffle(items)
        items = xsorted(items, key=lambda item: item[0])

        writer = csv.writer(sys.stdout)
        writer.writerow(headers)
        for item in items:
            writer.writerow(item)

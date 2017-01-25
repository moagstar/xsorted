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

    input_path = os.path.join(os.path.dirname(__file__), 'bnc-wordfreq.csv')
    with open(input_path) as fileobj:
        reader = csv.DictReader(fileobj)

        items = list(reader)
        random.shuffle(items)
        items = xsorted(items, key=lambda item: int(item['FREQUENCY']))

        writer = csv.DictWriter(sys.stdout, reader.fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

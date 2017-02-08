"""
example showing how xsorted can be used to sort csv files.
"""

import sys, csv, xsorted


with open('bnc-wordfreq.csv') as fileobj:
    reader = csv.DictReader(fileobj)
    items = xsorted.xsorted(reader, key=lambda x: int(x['FREQUENCY']))
    writer = csv.DictWriter(sys.stdout, reader.fieldnames)
    writer.writeheader()
    for item in items:
        writer.writerow(item)

import csv
import argparse

parser = argparse.ArgumentParser(description='Create Spettro product keywords')
parser.add_argument('-p', '--product-data', type=argparse.FileType('r'), help='Product data')
args = parser.parse_args()

with args.product_data as f:
    # Skip headers for product data
    product_reader = csv.reader(f)
    next(product_reader, None)
    occurred_words = {}
    for row in product_reader:
        name = row[0]
        desc = row[2]
        for word in desc.split(" "):
            if word in occurred_words:
                occurred_words[word] = occurred_words[word] + 1
            else:
                occurred_words[word] = 1
    black_list = [""]
    for key in occurred_words:
        if occurred_words[key] > 1:
            print(key, occurred_words[key])


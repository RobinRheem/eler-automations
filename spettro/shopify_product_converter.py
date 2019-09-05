import csv
import math
import argparse


parser = argparse.ArgumentParser(description='Create Shopfy product upload csv file. This is matched to Spettro atm.')
parser.add_argument('-p', '--product-data', type=argparse.FileType('r'), help='Product data')
parser.add_argument('-k', '--keywords', type=argparse.FileType('r'), help='Keywords')
parser.add_argument('-t', '--template', type=argparse.FileType('r'), help='Template header')
args = parser.parse_args()


# Setup keywords
keywords = {}
keyword_reader = csv.reader(args.keywords)
for row in keyword_reader:
    keywords[row[0]] = row[1]


def translate_description(desc):
    """Create hashtag body"""
    body = []
    for word in desc.split(" "):
        if word in keywords:
            body.append(f"#{keywords[word]}")
    return body


def translate_size(size):
    """Replace Korean related to size"""
    return (size.replace("프레임 사이즈", "Frame Size")
            .replace("앞쪽", "Front ")
            .replace("옆쪽", "Side")
            .replace("렌즈 사이즈", "Lens Size")
            .replace("가로", "Width")
            .replace("세로", "Height"))


# Create generated 
with args.product_data as f:
    # Get template headers
    template_reader = csv.reader(args.template)
    headers = next(template_reader, None)
    # Skip headers for product data
    product_reader = csv.reader(f)
    next(product_reader, None)
    # Create Shopify product csv
    shopify_products = open('spettro_products.csv', 'w')
    shopify_products.write(",".join(headers) + '\n')
    for row in product_reader:
        handle = row[0].replace(' ', '_').replace('(', '_').replace(')', '_').lower()
        title = row[0]
        tag = row[1].lower()
        size = translate_size(row[4].replace('\n', ' '))
        body = translate_description(row[3])
        info = " ".join(body)
        body = f'<p>{info}</p><p>{size}</p>'
        price = row[2].replace(',', '').replace('원', '')
        dollar_price = str(int(math.ceil(int(price) / 1000)))
        first_image = row[5]
        product_row_template = f'{handle},{title},{body},,,{tag},,Title,Default Title,,,,,,,,deny,manual,{dollar_price},,TRUE,TRUE,,{first_image},1,{tag},,,,,,,,,,,,,,,,,,g,,'
        shopify_products.write(product_row_template + '\n')
        for count, image_url in enumerate(list(filter(None, row[5:]))):
            product_image_template = f'{handle},,,,,,,,,,,,,,,,,,,,,,,{image_url},{count + 2},{tag},,,,,,,,,,,,,,,,,,,,'
            shopify_products.write(product_image_template + '\n')
    shopify_products.close()


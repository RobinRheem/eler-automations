import csv
import argparse


parser = argparse.ArgumentParser(description='Create Shopfy product upload csv file. This is matched to Spettro atm.')
parser.add_argument('-p', '--product-data', type=argparse.FileType('r'), help='Product data')
parser.add_argument('-k', '--keywords', type=argparse.FileType('r'), help='Keywords')
parser.add_argument('-t', '--template', type=argparse.FileType('r'), help='Template header')
args = parser.parse_args()

# Create generated 
with args.product_data as f:
    # Get template headers
    template_reader = csv.reader(args.template)
    headers = next(template_reader, None)
    # Create keyword dict
    keywords = {}
    keyword_reader = csv.reader(args.keywords)
    for row in keyword_reader:
        keywords[row[0]] = row[1]
    # Skip headers for product data
    product_reader = csv.reader(f)
    next(product_reader, None)
    # Create Shopify product csv
    shopify_products = open('spettro_products.csv', 'w')
    shopify_products.write(",".join(headers) + '\n')
    for row in product_reader:
        handle = row[0].replace(' ', '_').replace('(', '_').replace(')', '_').lower()
        title = row[0]
        desc = row[2]
        body = []
        for word in desc.split(" "):
            if word in keywords:
                body.append(f"#{keywords[word]}")
        #body = row[2].replace('\n', ' ') + ' ' + row[3].replace('\n', ' ')
        body = " ".join(body) + ' ' + row[3].replace('\n', ' ')
        price = row[1].replace(',', '').replace('원', '')
        first_image = row[4]
        product_row_template = f'{handle},{title},{body},,,,,,,,,,,,,,,,{price},,TRUE,TRUE,,{first_image},1,,,,,,,,,,,,,,,,,,,g,,'
        shopify_products.write(product_row_template + '\n')
        for count, image_url in enumerate(list(filter(None, row[4:]))):
            product_image_template = f'{handle},,,,,,,,,,,,,,,,,,,,,,,{image_url},{count + 2},,,,,,,,,,,,,,,,,,,,,'
            shopify_products.write(product_image_template + '\n')
    shopify_products.close()


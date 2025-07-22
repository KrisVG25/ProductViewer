import pandas as pd
import os

def parse_excel(filepath, image_folder):
    df = pd.read_excel(filepath)

    attributes = [col for col in df.columns if col.startswith('ATT')]
    distributions = [col for col in df.columns if col.startswith('DIST')]
    price_col = df.columns[-1] if 'price' in df.columns[-1].lower() else None

    print("Detected price column:", price_col)


    products = []
    for _, row in df.iterrows():
        image_id = str(row[0])
        img_path_jpg = os.path.join(image_folder, image_id + '.jpg')
        img_path_png = os.path.join(image_folder, image_id + '.png')
        img_path = None

        if os.path.exists(img_path_jpg):
            img_path = img_path_jpg
        elif os.path.exists(img_path_png):
            img_path = img_path_png
        else:
            img_path = os.path.join(image_folder, 'notFound.png')

        price = f"${row[price_col]:.2f}" if price_col and not pd.isna(row[price_col]) else ""
        description = f"{row[1]} {price}".strip()

        print(f"Parsed product: {description}")

        product = {
            'image': img_path,
            'description': description,
            'attributes': {attr: row[attr] for attr in attributes},
            'distributions': {dist: 'X' in str(row[dist]).upper() for dist in distributions}
        }
        products.append(product)

    return products, attributes, distributions

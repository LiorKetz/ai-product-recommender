import json
from pathlib import Path
from db.categories_map import category_map
CATALOG_PATH = Path(__file__).parent / 'db' / 'products.json'


with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    PRODUCT_CATALOG = json.load(f)


def get_product_catalog():
    return PRODUCT_CATALOG


def get_product_keys():
    if not PRODUCT_CATALOG:
        return []
    return list(PRODUCT_CATALOG[0].keys())


def get_categories():
    return list(category_map.keys())


def get_products_by_category(category_name: str):
    skus = category_map.get(category_name, [])
    return [p for p in PRODUCT_CATALOG if p["SKU"] in skus]
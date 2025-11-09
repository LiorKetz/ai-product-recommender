import json
from pathlib import Path
from db.categories_map import category_map
CATALOG_PATH = Path(__file__).parent / 'db' / 'products.json'

# Load product catalog once at module load time
with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
    PRODUCT_CATALOG = json.load(f)


def get_product_catalog():
    """
    Get the full product catalog.
    
    Returns:
        List[Dict]: The product catalog.
    """
    return PRODUCT_CATALOG


def get_product_keys():
    """
    Get the keys of the product catalog items.

    Returns:
        List[str]: The keys of the product items.
    """
    if not PRODUCT_CATALOG:
        return []
    return list(PRODUCT_CATALOG[0].keys())


def get_categories():
    """
    Get the list of product categories.

    Returns:
        List[str]: The list of product categories.
    """
    return list(category_map.keys())


def get_products_by_category(category_name: str):
    """
    Get products by category name.
    
    Parameters:
        category_name (str): The name of the category.
    Returns:
        List[Dict]: The list of products in the specified category.
    """
    skus = category_map.get(category_name, [])
    return [p for p in PRODUCT_CATALOG if p["SKU"] in skus]
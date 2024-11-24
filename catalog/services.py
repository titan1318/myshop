from django.core.cache import cache
from catalog.models import Category, Product


def get_categories():
    cache_key = 'categories_list'
    categories = cache.get(cache_key)

    if not categories:
        categories = list(Category.objects.all())
        cache.set(cache_key, categories, timeout=900)
    return categories


def get_products():
    cache_key = 'products_list'
    products = cache.get(cache_key)

    if not products:
        products = list(Product.objects.all())
        cache.set(cache_key, products, timeout=900)

    return products

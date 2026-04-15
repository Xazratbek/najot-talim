from .models import Category, Product


def category_all(offset=None, limit=None):
    query = Category.objects.all().order_by('-id')
    if limit and offset is None:
        return query[:limit]
    if limit and offset:
        return query[offset:limit]
    return query

def parent_categories(offset=None, limit=None):
    query = Category.objects.filter(parent__isnull=True).order_by('-id')
    if limit and offset is None:
        return query[:limit]
    if limit and offset:
        return query[offset:limit]
    return query

def discount_desc(offset=None, limit=None):
    query = Product.objects.filter(discount__gt =0).order_by('-discount')
    if limit and offset is None:
        return query[:limit]
    if limit and offset:
        return query[offset:limit]

    return query

def category_unique_product():
    return (Product.objects.filter(category = category).first() for category in category_all() if Product.objects.filter(category = category))

def new_arrivals():
    return Product.objects.all().order_by("-created_at")

def featured_products():
    return Product.objects.filter(is_featured=True)
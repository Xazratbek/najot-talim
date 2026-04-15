
import os
import django
import random
from faker import Faker
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from users.models import CustomUser
from products.models import Category, Product, ProductImage, Comment, Saved, RecentlyProduct, ProductView
from orders.models import Card, CardItem, Order, OrderItem
from home.models import Slider, Banner, Brand
from blog.models import Post

fake = Faker()

def generate_data():
    from django.db import transaction

    with transaction.atomic():
        print("Clearing existing data...")
        # Clear existing data in the correct order
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CardItem.objects.all().delete()
        Card.objects.all().delete()
        Comment.objects.all().delete()
        Saved.objects.all().delete()
        RecentlyProduct.objects.all().delete()
        ProductView.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Post.objects.all().delete()
        Slider.objects.all().delete()
        Banner.objects.all().delete()
        Brand.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()
        print("Data cleared.")

        # Generate Users
        print("Generating users...")
        users = []
        for i in range(10):
            print(f"Generating user {i+1}/10")
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                password='password123',
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()
            )
            users.append(user)
        print("Users generated.")

        # Generate Categories
        print("Generating categories...")
        categories = []
        for i in range(5):
            print(f"Generating category {i+1}/5")
            category = Category.objects.create(title=fake.word())
            categories.append(category)
        print("Categories generated.")

        # Generate Products
        print("Generating products...")
        products = []
        for i, user in enumerate(users):
            for j in range(2):
                print(f"Generating product {j+1}/2 for user {i+1}/{len(users)}")
                product = Product.objects.create(
                    title=fake.sentence(nb_words=3),
                    desc=fake.text(),
                    price=round(random.uniform(10.0, 500.0), 2),
                    discount=random.randint(5, 50) if random.choice([True, False]) else None,
                    user=user,
                    category=random.choice(categories),
                    is_featured=random.choice([True, False])
                )
                products.append(product)
        print("Products generated.")

        # Generate Product Images
        print("Generating product images...")
        for i, product in enumerate(products):
            print(f"Generating images for product {i+1}/{len(products)}")
            for _ in range(random.randint(1, 2)):
                try:
                    image_url = 'https://picsum.photos/300/300'
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        ProductImage.objects.create(
                            product=product,
                            photo=ContentFile(response.content, name=f'{product.id}_{fake.uuid4()}.jpg')
                        )
                except Exception as e:
                    print(f"Error downloading image: {e}")
        print("Product images generated.")


        # Generate Comments
        print("Generating comments...")
        for i, user in enumerate(users):
            print(f"Generating comments for user {i+1}/{len(users)}")
            for product in random.sample(products, k=5):
                if not Comment.objects.filter(user=user, product=product).exists():
                    Comment.objects.create(
                        product=product,
                        user=user,
                        text=fake.sentence(),
                        rate=random.randint(1, 5)
                    )
        print("Comments generated.")

        # Generate Saved Products
        print("Generating saved products...")
        for i, user in enumerate(users):
            print(f"Generating saved products for user {i+1}/{len(users)}")
            for product in random.sample(products, k=5):
                if not Saved.objects.filter(user=user, product=product).exists():
                    Saved.objects.create(product=product, user=user)
        print("Saved products generated.")

        # Generate Recently Viewed Products
        print("Generating recently viewed products...")
        for i, user in enumerate(users):
            print(f"Generating recently viewed products for user {i+1}/{len(users)}")
            for product in random.sample(products, k=5):
                if not RecentlyProduct.objects.filter(user=user, product=product).exists():
                    RecentlyProduct.objects.create(product=product, user=user)
        print("Recently viewed products generated.")

        # Generate Product Views
        print("Generating product views...")
        for i, product in enumerate(products):
            print(f"Generating views for product {i+1}/{len(products)}")
            for _ in range(random.randint(0, 20)):
                ProductView.objects.create(product=product)
        print("Product views generated.")

        # Generate Cards and CardItems
        print("Generating cards and card items...")
        for i, user in enumerate(users):
            print(f"Generating card and items for user {i+1}/{len(users)}")
            card, _ = Card.objects.get_or_create(user=user)
            for product in random.sample(products, k=random.randint(1, 3)):
                if not CardItem.objects.filter(card=card, product=product).exists():
                    CardItem.objects.create(
                        card=card,
                        product=product,
                        quantity=random.randint(1, 3)
                    )
        print("Cards and card items generated.")

        # Generate Orders and OrderItems
        print("Generating orders and order items...")
        for i, user in enumerate(users):
            print(f"Generating orders for user {i+1}/{len(users)}")
            for _ in range(random.randint(1, 2)):
                order = Order.objects.create(
                    user=user,
                    address=fake.address(),
                    status=random.choice([s[0] for s in Order.STATUS])
                )
                for product in random.sample(products, k=random.randint(1, 3)):
                    order_item_quantity = random.randint(1, 2)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=order_item_quantity,
                        total_price=product.final_price * order_item_quantity
                    )
        print("Orders and order items generated.")

        # Generate Sliders
        print("Generating sliders...")
        for i in range(2):
            print(f"Generating slider {i+1}/2")
            try:
                image_url = 'https://picsum.photos/1200/400'
                response = requests.get(image_url)
                if response.status_code == 200:
                    Slider.objects.create(
                        title=fake.sentence(),
                        description=fake.text(),
                        url=fake.url(),
                        image=ContentFile(response.content, name=f'slider_{fake.uuid4()}.jpg')
                    )
            except Exception as e:
                print(f"Error downloading image: {e}")
        print("Sliders generated.")


        # Generate Banners
        print("Generating banners...")
        for i in range(2):
            print(f"Generating banner {i+1}/2")
            try:
                image_url = 'https://picsum.photos/600/300'
                response = requests.get(image_url)
                if response.status_code == 200:
                    Banner.objects.create(
                        url=fake.url(),
                        position=fake.word(),
                        image=ContentFile(response.content, name=f'banner_{fake.uuid4()}.jpg')
                    )
            except Exception as e:
                print(f"Error downloading image: {e}")
        print("Banners generated.")


        # Generate Brands
        print("Generating brands...")
        for i in range(5):
            print(f"Generating brand {i+1}/5")
            try:
                image_url = 'https://picsum.photos/150/150'
                response = requests.get(image_url)
                if response.status_code == 200:
                    Brand.objects.create(
                        name=fake.company(),
                        logo=ContentFile(response.content, name=f'brand_{fake.uuid4()}.jpg')
                    )
            except Exception as e:
                print(f"Error downloading image: {e}")
        print("Brands generated.")

        # Generate Blog Posts
        print("Generating blog posts...")
        for i in range(5):
            print(f"Generating post {i+1}/5")
            try:
                image_url = 'https://picsum.photos/800/600'
                response = requests.get(image_url)
                if response.status_code == 200:
                    Post.objects.create(
                        title=fake.sentence(),
                        content=fake.text(),
                        image=ContentFile(response.content, name=f'post_{fake.uuid4()}.jpg')
                    )
            except Exception as e:
                print(f"Error downloading image: {e}")
        print("Blog posts generated.")

    print("Data generation complete.")

if __name__ == '__main__':
    generate_data()

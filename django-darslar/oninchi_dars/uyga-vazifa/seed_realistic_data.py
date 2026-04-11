import argparse
import os
import random
import shutil
import ssl
import urllib.error
import urllib.request
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from categories.models import Category
from chat.models import ChatRoom, Message
from favorites.models import Favorite
from listings.models import CurrencyChoice, Listing, ListingImage, StatusChoice
from reviews.models import Review


SEED_VALUE = 42
random.seed(SEED_VALUE)

USER_COUNT = 180
LISTING_COUNT = 900
FAVORITE_COUNT = 2800
CHATROOM_COUNT = 520
MESSAGE_TARGET = 4800
REVIEW_COUNT = 420
LISTING_IMAGE_POOL_SIZE = 120
AVATAR_POOL_SIZE = 36

MEDIA_ROOT = Path(settings.MEDIA_ROOT)
LISTING_IMAGE_DIR = MEDIA_ROOT / "listings" / "seed"
AVATAR_IMAGE_DIR = MEDIA_ROOT / "users" / "seed"
CATEGORY_ICON_DIR = MEDIA_ROOT / "category_icons" / "seed"

PICSUM_IDS = [
    10, 11, 12, 14, 15, 16, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 34, 35,
    36, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 52, 54, 55, 57, 58,
    59, 60, 61, 62, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78, 79,
    80, 82, 83, 84, 85, 87, 88, 89, 91, 92, 93, 94, 95, 96, 98, 99, 100, 101,
    102, 103, 104, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117, 118, 119,
    120, 121, 122, 123, 124, 126, 127, 129, 130, 132, 133, 134, 136, 137, 139,
    141, 142, 143, 144, 145, 146, 147, 149, 151, 152, 153, 154, 155, 156, 157,
    158, 159, 160, 161, 162, 163, 164, 165, 167, 168, 169, 170, 171, 172, 173,
]

FIRST_NAMES = [
    "Aziza", "Dilshod", "Jasur", "Madina", "Shahzod", "Sarvinoz", "Bekzod",
    "Nigora", "Sardor", "Maftuna", "Akmal", "Zarnigor", "Sherzod", "Nilufar",
    "Baxtiyor", "Fotima", "Oybek", "Sevara", "Ulugbek", "Mohira", "Davron",
    "Gulnoza", "Kamron", "Malika", "Rustam", "Rayhona", "Doniyor", "Umida",
    "Anvar", "Shahnoza", "Islom", "Gulruh", "Bobur", "Shoira", "Asadbek",
    "Feruza", "Ibrohim", "Munisa", "Muhammadali", "Shaxlo", "Mirjalol",
    "Dildora", "Abdulaziz", "Kamola", "Laziz", "Nargiza", "Temur", "Shahina",
    "Otabek", "Sabina", "Abbos", "Mubina", "Suhrob", "Marjona", "Shukrulloh",
    "Ziyoda", "Komil", "Hilola", "Abdulloh", "Mashhura", "Shahriyor", "Bonu",
]

LAST_NAMES = [
    "Karimov", "Rasulov", "Abdullayev", "Tursunov", "Nazarov", "Yusupov",
    "Qodirov", "Alimuhamedov", "Ergashev", "Usmonov", "Xudoyberdiyev",
    "Rahimov", "Sobirov", "Tojiyev", "Mamatqulov", "Sodiqov", "Haydarov",
    "Komilova", "Rustamova", "Asqarova", "Normatova", "Yoqubova", "Fayziyeva",
    "Saidova", "Teshaboyeva", "Shukurova", "Mirzayeva", "Jalilova", "Tursunova",
    "Abduqodirov", "Ismoilov", "Qurbonov", "Erkinov", "Jo'rayev", "Sattorov",
]

UZBEK_CITIES = [
    "Toshkent", "Samarqand", "Buxoro", "Andijon", "Farg'ona", "Namangan",
    "Qarshi", "Nukus", "Urganch", "Jizzax", "Termiz", "Navoiy", "Qo'qon",
    "Marg'ilon", "Chirchiq", "Bekobod", "Angren", "Xiva", "Denov", "Guliston",
]

NEIGHBORHOODS = {
    "Toshkent": ["Yunusobod", "Chilonzor", "Mirobod", "Olmazor", "Sergeli"],
    "Samarqand": ["Registon", "Siab", "Kimyogarlar", "Bog'ishamol"],
    "Buxoro": ["Gijduvon", "Kogon", "Markaz", "Saxovat"],
    "Andijon": ["Asaka", "Shahrixon", "Markaz", "Paxtaobod"],
    "Farg'ona": ["Marg'ilon yo'li", "Qirguli", "Quvasoy", "Markaz"],
}

LISTING_OPENERS = [
    "Toza ishlaydi, uy sharoitida ishlatilgan.",
    "Holati yaxshi, hamma funksiyasi ishlaydi.",
    "Magazindan qolgan yangi mahsulot, kafolat taloni bor.",
    "Kam ishlatilgan, ko'rinishi ham, ishlashi ham yaxshi.",
    "Shaxsiy foydalanish uchun olingan, hozir kerak bo'lmay qoldi.",
    "Usta ko'rgan, ishlashi tekshirilgan.",
    "Sotuvga qo'yishdan oldin tozalab tayyorlangan.",
]

LISTING_DETAILS = [
    "Rasmlarda ko'rinib turgan holatda.",
    "Jiddiy oluvchiga joyida ko'rsataman.",
    "Faqat real oluvchilar murojaat qilsin.",
    "Narx ozgina kelishiladi.",
    "Qo'shimcha savollar bo'lsa, chat orqali yozing.",
    "Bir qo'l ishlatilgan, ehtiyot bilan foydalanganmiz.",
    "Tuman markazida ko'rsatib beraman.",
]

MESSAGE_SAMPLES = [
    "Assalomu alaykum, e'lon hali aktivmi?",
    "Narxini ozroq tushirishning iloji bormi?",
    "Bugun borib ko'rsam bo'ladimi?",
    "Mahsulotda biror aybi yo'qmi?",
    "Telegram orqali bog'lansak bo'ladimi?",
    "Qaysi tumandasiz?",
    "Komplektida yana nimalar bor?",
    "Oxirgi narxini aytsangiz olaman.",
    "Yetkazib berish qilasizmi yoki olib ketamanmi?",
    "Rasmdagidek holatdami, yangi tushganmi?",
    "Buni kechqurun olib ketishga ulguramanmi?",
    "Hujjatlari joyidami?",
]

REVIEW_COMMENTS = [
    "Sotuvchi juda muloyim ekan, mahsulot ham tavsifdagidek chiqdi.",
    "Vaqtida javob berdi, narx yuzasidan ham kelishdik.",
    "Mahsulot toza holatda ekan, tavsiya qilaman.",
    "Bitim yaxshi o'tdi, yana savdo qilish mumkin.",
    "Savollarga aniq javob berdi, muomala yaxshi.",
    "Rasm va tavsifga mos mahsulot oldim.",
    "Biroz kechikdi, lekin umumiy taassurot yaxshi.",
    "Sotuvchi halol ekan, bemalol ishlasa bo'ladi.",
    "Ko'rsatgan narsasi aynan o'sha ekan.",
    "Aloqaga tez chiqdi, bitim oson bo'ldi.",
]

CATEGORY_TREE = {
    "Transport": [
        "Yengil avtomobillar", "Motosikllar", "Avto ehtiyot qismlar",
        "Avtoaudio va elektronika", "Shinalar va disklar",
    ],
    "Ko'chmas mulk": [
        "Kvartiralar", "Hovli-joylar", "Noturar joy", "Ijaraga kvartira",
        "Yer uchastkalari",
    ],
    "Elektronika": [
        "Smartfonlar", "Noutbuklar", "Televizorlar", "Planshetlar",
        "Aksessuarlar",
    ],
    "Maishiy texnika": [
        "Sovutgichlar", "Kir yuvish mashinalari", "Konditsionerlar",
        "Changyutgichlar", "Gaz plitalar",
    ],
    "Mebel va interyer": [
        "Divanlar", "Stollar", "Shkaflar", "Oshxona mebellari", "Yoritish",
    ],
    "Bolalar dunyosi": [
        "Aravachalar", "Bolalar kiyimi", "O'yinchoqlar", "Maktab anjomlari",
        "Velosipedlar",
    ],
    "Kiyim-kechak": [
        "Erkaklar kiyimi", "Ayollar kiyimi", "Poyabzal", "Sumkalar",
        "Aksessuarlar",
    ],
    "Uy va bog'": [
        "Qurilish mollari", "Bog' jihozlari", "Uy dekorlari", "Idish-tovoqlar",
        "Tozalash vositalari",
    ],
    "Sport va hobbi": [
        "Velosipedlar", "Trenajyorlar", "Baliq ovlash", "Musiqa asboblari",
        "O'yin konsollari",
    ],
    "Ish va xizmatlar": [
        "Ta'mirlash xizmatlari", "Kuryerlik", "Dizayn xizmati",
        "O'quv kurslari", "Santexnika ishlari",
    ],
}

BRANDS = {
    "Smartfonlar": ["Apple", "Samsung", "Xiaomi", "Infinix", "Tecno"],
    "Noutbuklar": ["Lenovo", "HP", "Dell", "Asus", "Acer"],
    "Televizorlar": ["Artel", "Samsung", "LG", "Shivaki", "Sony"],
    "Planshetlar": ["Apple", "Samsung", "Huawei", "Xiaomi"],
    "Sovutgichlar": ["Artel", "Samsung", "LG", "Midea", "Avalon"],
    "Kir yuvish mashinalari": ["Samsung", "LG", "Artel", "Bosch", "Indesit"],
    "Konditsionerlar": ["Artel", "Midea", "Avalon", "Shivaki", "Ziffler"],
    "Changyutgichlar": ["Samsung", "LG", "Bosch", "Artel"],
    "Gaz plitalar": ["Artel", "Gefest", "Beko", "Shivaki"],
    "Yengil avtomobillar": ["Chevrolet", "Kia", "Hyundai", "BYD"],
    "Motosikllar": ["Lifan", "Yamaha", "Honda", "Voge"],
}

TITLE_PATTERNS = {
    "Smartfonlar": [
        "{brand} {model} {storage}GB",
        "{brand} {model} ideal holatda",
        "{brand} {model} komplekt bilan",
    ],
    "Noutbuklar": [
        "{brand} {model} noutbuk",
        "{brand} {model} ofis uchun",
        "{brand} {model} studentlar uchun qulay",
    ],
    "Sovutgichlar": [
        "{brand} {model} sovutgich",
        "{brand} {model} deyarli yangi",
        "{brand} katta hajmli sovutgich",
    ],
}

GENERIC_MODELS = [
    "2022", "2023", "Pro", "Max", "Plus", "Air", "Neo", "Prime", "X5", "A13",
    "S21", "14 Pro", "15", "Note 12", "MDRT645", "NF310", "IdeaPad 3",
    "Vostro 3520", "Pavilion 15", "Aspire 5", "Spark", "Cobalt", "Monza",
]


def unique_username(first_name, last_name, used_usernames):
    base = slugify(f"{first_name}.{last_name}") or "foydalanuvchi"
    candidate = base
    counter = 1
    while candidate in used_usernames:
        counter += 1
        candidate = f"{base}{counter}"
    used_usernames.add(candidate)
    return candidate


def random_phone(index):
    return f"+998{random.choice(['90', '91', '93', '94', '95', '97', '98', '99'])}{index:07d}"


def random_past_datetime(days=365):
    now = timezone.now()
    return now - timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


def set_timestamps(obj, created_at):
    updated_at = created_at + timedelta(days=random.randint(0, 40), hours=random.randint(0, 12))
    if updated_at > timezone.now():
        updated_at = timezone.now()
    obj.__class__.objects.filter(pk=obj.pk).update(created_at=created_at, updated_at=updated_at)


def ensure_directories():
    LISTING_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    AVATAR_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORY_ICON_DIR.mkdir(parents=True, exist_ok=True)


def download_file(url, target_path):
    try:
        with urllib.request.urlopen(url, timeout=20) as response, open(target_path, "wb") as output:
            output.write(response.read())
    except urllib.error.URLError as exc:
        if not isinstance(exc.reason, ssl.SSLCertVerificationError):
            raise
        insecure_context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, timeout=20, context=insecure_context) as response, open(target_path, "wb") as output:
            output.write(response.read())
    except ssl.SSLCertVerificationError:
        insecure_context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, timeout=20, context=insecure_context) as response, open(target_path, "wb") as output:
            output.write(response.read())


def ensure_real_image_pool():
    ensure_directories()
    listing_pool = []
    avatar_pool = []

    for idx, picsum_id in enumerate(PICSUM_IDS[:LISTING_IMAGE_POOL_SIZE], start=1):
        file_name = f"listing-seed-{idx:03d}.jpg"
        path = LISTING_IMAGE_DIR / file_name
        if not path.exists():
            download_file(f"https://picsum.photos/id/{picsum_id}/1200/900.jpg", path)
        listing_pool.append(Path("listings") / "seed" / file_name)

    avatar_ids = PICSUM_IDS[LISTING_IMAGE_POOL_SIZE:LISTING_IMAGE_POOL_SIZE + AVATAR_POOL_SIZE]
    for idx, picsum_id in enumerate(avatar_ids, start=1):
        file_name = f"avatar-seed-{idx:03d}.jpg"
        path = AVATAR_IMAGE_DIR / file_name
        if not path.exists():
            download_file(f"https://picsum.photos/id/{picsum_id}/400/400.jpg", path)
        avatar_pool.append(Path("users") / "seed" / file_name)

    return listing_pool, avatar_pool


def reset_seed_data():
    Message.objects.all().delete()
    ChatRoom.objects.all().delete()
    Favorite.objects.all().delete()
    Review.objects.all().delete()
    ListingImage.objects.all().delete()
    Listing.objects.all().delete()
    Category.objects.all().delete()
    User = get_user_model()
    User.objects.exclude(is_superuser=True).delete()

    for path in [LISTING_IMAGE_DIR, AVATAR_IMAGE_DIR, CATEGORY_ICON_DIR]:
        if path.exists():
            shutil.rmtree(path)


def create_category_icons(count):
    icons = []
    for idx, picsum_id in enumerate(PICSUM_IDS[-count:], start=1):
        file_name = f"category-icon-{idx:03d}.jpg"
        path = CATEGORY_ICON_DIR / file_name
        if not path.exists():
            download_file(f"https://picsum.photos/id/{picsum_id}/240/240.jpg", path)
        icons.append(Path("category_icons") / "seed" / file_name)
    return icons


def create_categories():
    category_icon_pool = create_category_icons(len(CATEGORY_TREE) + 10)
    created = []
    icon_index = 0
    for parent_name, children in CATEGORY_TREE.items():
        parent, _ = Category.objects.get_or_create(
            name=parent_name,
            parent=None,
            defaults={"icon": str(category_icon_pool[icon_index % len(category_icon_pool)])},
        )
        icon_index += 1
        created.append(parent)
        for child_name in children:
            child, _ = Category.objects.get_or_create(
                name=child_name,
                parent=parent,
                defaults={"icon": str(category_icon_pool[icon_index % len(category_icon_pool)])},
            )
            icon_index += 1
            created.append(child)
    return created


def create_users(avatar_pool):
    User = get_user_model()
    users = []
    used_usernames = set(User.objects.values_list("username", flat=True))

    for index in range(1, USER_COUNT + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = unique_username(first_name, last_name, used_usernames)
        email = f"{username}@mail.uz"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": random_phone(index),
                "avatar": str(random.choice(avatar_pool)),
            },
        )
        if created:
            user.set_password("test12345")
            user.save(update_fields=["password"])
            set_timestamps(user, random_past_datetime())
        users.append(user)
    return users


def leaf_category_text(category):
    if category.parent:
        return f"{category.parent.name} / {category.name}"
    return category.name


def random_district(city):
    return random.choice(NEIGHBORHOODS.get(city, ["Markaz", "Yangiobod", "Guliston", "Saxovat"]))


def listing_price_for_category(category_name):
    if category_name in {"Smartfonlar", "Planshetlar"}:
        return Decimal(random.randrange(180, 1400) * 10000)
    if category_name == "Noutbuklar":
        return Decimal(random.randrange(250, 2200) * 10000)
    if category_name in {"Televizorlar", "Sovutgichlar", "Kir yuvish mashinalari", "Konditsionerlar"}:
        return Decimal(random.randrange(220, 2600) * 10000)
    if category_name == "Yengil avtomobillar":
        return Decimal(random.randrange(4500, 42000) * 10000)
    if category_name == "Kvartiralar":
        return Decimal(random.randrange(25000, 160000) * 10000)
    return Decimal(random.randrange(25, 1800) * 10000)


def listing_currency(category_name):
    if category_name in {"Yengil avtomobillar", "Kvartiralar", "Noutbuklar", "Sovutgichlar"}:
        return random.choice([CurrencyChoice.UZS, CurrencyChoice.USD, CurrencyChoice.USD])
    return random.choice([CurrencyChoice.UZS, CurrencyChoice.UZS, CurrencyChoice.USD])


def listing_title(category):
    brand = random.choice(BRANDS.get(category.name, ["Universal", "Artel", "Samsung", "Chevrolet"]))
    model = random.choice(GENERIC_MODELS)
    storage = random.choice([64, 128, 256, 512])
    patterns = TITLE_PATTERNS.get(
        category.name,
        [
            f"{category.name} yaxshi holatda",
            f"{brand} {category.name.lower()} sotiladi",
            f"{leaf_category_text(category)} arzon narxda",
        ],
    )
    pattern = random.choice(patterns)
    return pattern.format(brand=brand, model=model, storage=storage)


def listing_description(category, city):
    district = random_district(city)
    sentences = [
        random.choice(LISTING_OPENERS),
        f"{leaf_category_text(category)} bo'yicha e'lon {city} shahri, {district} hududidan joylandi.",
        random.choice(LISTING_DETAILS),
    ]
    return " ".join(sentences)


def create_listings(users):
    leaf_categories = list(Category.objects.filter(categories__isnull=True))
    listings = []

    for _ in range(LISTING_COUNT):
        owner = random.choice(users)
        category = random.choice(leaf_categories)
        city = random.choice(UZBEK_CITIES)
        listing = Listing.objects.create(
            title=listing_title(category),
            description=listing_description(category, city),
            price=listing_price_for_category(category.name),
            currency=listing_currency(category.name),
            listing_category=category,
            user=owner,
            condition=random.choice(["new", "used", "used", "used"]),
            city=city,
            status=random.choice(
                [StatusChoice.ACTIVE, StatusChoice.ACTIVE, StatusChoice.ACTIVE, StatusChoice.ACTIVE, StatusChoice.SOLD, StatusChoice.ARCHIVED]
            ),
            view_count=random.randint(15, 18000),
        )
        set_timestamps(listing, random_past_datetime())
        listings.append(listing)

    return listings


def create_listing_images(listings, listing_pool):
    created_count = 0
    for listing in listings:
        image_count = random.randint(2, 5)
        chosen_images = random.sample(listing_pool, image_count)
        for order, image_path in enumerate(chosen_images):
            ListingImage.objects.create(
                listing=listing,
                image=str(image_path),
                is_main=order == 0,
            )
            created_count += 1
    return created_count


def create_favorites(users, listings):
    existing_pairs = set(Favorite.objects.values_list("user_id", "favorite_listing_id"))
    created_count = 0
    attempts = 0

    while created_count < FAVORITE_COUNT and attempts < FAVORITE_COUNT * 10:
        attempts += 1
        user = random.choice(users)
        listing = random.choice(listings)
        pair = (user.pk, listing.pk)
        if listing.user_id == user.pk or pair in existing_pairs:
            continue
        favorite = Favorite.objects.create(user=user, favorite_listing=listing)
        set_timestamps(favorite, random_past_datetime())
        existing_pairs.add(pair)
        created_count += 1

    return created_count


def create_chatrooms(users, listings):
    rooms = []
    existing_pairs = set(ChatRoom.objects.values_list("chat_listing_id", "buyer_id"))
    active_listings = [listing for listing in listings if listing.status == StatusChoice.ACTIVE]
    attempts = 0

    while len(rooms) < CHATROOM_COUNT and attempts < CHATROOM_COUNT * 12:
        attempts += 1
        listing = random.choice(active_listings)
        buyer = random.choice(users)
        pair = (listing.pk, buyer.pk)
        if buyer.pk == listing.user_id or pair in existing_pairs:
            continue
        room = ChatRoom.objects.create(
            chat_listing=listing,
            buyer=buyer,
            seller=listing.user,
        )
        set_timestamps(room, random_past_datetime())
        existing_pairs.add(pair)
        rooms.append(room)

    return rooms


def create_messages(rooms):
    created_count = 0
    for room in rooms:
        message_count = random.randint(6, 14)
        for _ in range(message_count):
            sender = random.choice([room.buyer, room.seller])
            created_at = room.created_at + timedelta(minutes=random.randint(1, 4200))
            message = Message.objects.create(
                room=room,
                sender=sender,
                text=random.choice(MESSAGE_SAMPLES),
                is_read=random.choice([True, True, True, False]),
            )
            set_timestamps(message, created_at)
            created_count += 1
            if created_count >= MESSAGE_TARGET:
                return created_count
    return created_count


def create_reviews(users):
    created_count = 0
    existing_pairs = set(Review.objects.values_list("reviewer_id", "target_user_id"))
    attempts = 0

    while created_count < REVIEW_COUNT and attempts < REVIEW_COUNT * 10:
        attempts += 1
        reviewer = random.choice(users)
        target_user = random.choice(users)
        pair = (reviewer.pk, target_user.pk)
        if reviewer.pk == target_user.pk or pair in existing_pairs:
            continue
        review = Review.objects.create(
            reviewer=reviewer,
            target_user=target_user,
            rating=random.choices([5, 4, 3, 2], weights=[48, 29, 17, 6], k=1)[0],
            comment=random.choice(REVIEW_COMMENTS),
        )
        set_timestamps(review, random_past_datetime())
        existing_pairs.add(pair)
        created_count += 1

    return created_count


@transaction.atomic
def seed(reset=False):
    if reset:
        reset_seed_data()

    listing_pool, avatar_pool = ensure_real_image_pool()
    categories = create_categories()
    users = create_users(avatar_pool)
    listings = create_listings(users)
    listing_images_count = create_listing_images(listings, listing_pool)
    favorites_count = create_favorites(users, listings)
    rooms = create_chatrooms(users, listings)
    messages_count = create_messages(rooms)
    reviews_count = create_reviews(users)

    print("Seed yakunlandi:")
    print(f"- Category: {len(categories)} ta")
    print(f"- User: {len(users)} ta")
    print(f"- Listing: {len(listings)} ta")
    print(f"- ListingImage: {listing_images_count} ta")
    print(f"- Favorite: {favorites_count} ta")
    print(f"- ChatRoom: {len(rooms)} ta")
    print(f"- Message: {messages_count} ta")
    print(f"- Review: {reviews_count} ta")
    print(f"- Listing image pool: {len(listing_pool)} ta real rasm")
    print(f"- Avatar image pool: {len(avatar_pool)} ta real rasm")
    print("Test parol: test12345")


def parse_args():
    parser = argparse.ArgumentParser(description="Marketplace uchun realistik seed data yaratadi.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Mavjud seeded ma'lumotlarni o'chirib, qaytadan to'ldiradi.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    seed(reset=args.reset)

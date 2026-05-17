"""
Seed demo data: categories, products, banners, reviews, users
Usage: python manage.py seed_data
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Category, Brand, Product, Banner, Coupon
from reviews.models import Review

User = get_user_model()

CATEGORIES = [
    ("Electronics", "bi-laptop", "Cutting-edge tech and gadgets"),
    ("Fashion", "bi-bag-heart", "Premium apparel and accessories"),
    ("Home & Living", "bi-house-heart", "Beautiful furniture and décor"),
    ("Beauty", "bi-stars", "Skincare and beauty essentials"),
    ("Sports", "bi-bicycle", "Gear for every activity"),
    ("Books", "bi-book", "Knowledge and inspiration"),
    ("Jewelry", "bi-gem", "Fine jewelry and watches"),
    ("Gaming", "bi-controller", "Games and gaming accessories"),
]

BRANDS = ["Apple", "Samsung", "Sony", "Nike", "Adidas", "Zara", "H&M", "IKEA", "Dyson", "LG"]

PRODUCTS = [
    # Electronics
    ("Wireless Noise-Cancelling Headphones", "Electronics", 299.99, 199.99, True, True, False, True, 45,
     "Premium sound isolation with 30-hour battery life and ultra-comfortable cushioning. Experience music the way the artist intended.", True),
    ("Ultra-Slim Laptop 15\"", "Electronics", 1299.99, 999.99, True, True, True, False, 12,
     "Feather-light design meets powerhouse performance. 12-hour battery, stunning OLED display, lightning-fast SSD storage.", True),
    ("Smart Watch Pro Series 5", "Electronics", 499.99, 379.99, False, True, True, True, 8,
     "Your health command center on your wrist. Track fitness, sleep, ECG, and stay connected all day.", True),
    ("4K OLED TV 55\"", "Electronics", 1499.99, 1099.99, True, False, False, True, 20,
     "Cinematic picture quality with infinite contrast. Every scene bursts to life with vivid, accurate color.", True),
    ("True Wireless Earbuds", "Electronics", 149.99, 99.99, False, True, True, False, 60,
     "Crystal-clear audio in a compact design. 8-hour playback per charge plus 24 hours from the case.", False),
    ("Mechanical Keyboard RGB", "Electronics", 189.99, 149.99, False, False, True, True, 35,
     "Tactile precision for gamers and typists. Per-key RGB lighting, N-key rollover, aircraft-grade aluminum body.", False),

    # Fashion
    ("Classic Leather Oxford Shoes", "Fashion", 189.99, 129.99, True, True, False, True, 25,
     "Handcrafted from full-grain leather with a Goodyear-welted sole. The Oxford that elevates every outfit.", True),
    ("Cashmere Turtleneck Sweater", "Fashion", 249.99, None, True, False, True, True, 18,
     "Grade-A Mongolian cashmere. Impossibly soft, effortlessly chic, built to last a lifetime.", True),
    ("Slim-Fit Chino Pants", "Fashion", 89.99, 59.99, False, True, True, False, 50,
     "Modern cut with stretch comfort fabric. Wrinkle-resistant and versatile for office or weekend.", False),
    ("Silk Evening Dress", "Fashion", 329.99, 249.99, True, True, False, True, 10,
     "100% mulberry silk with elegant drape. Hand-finished details and a flattering bias cut.", True),
    ("Designer Crossbody Bag", "Fashion", 399.99, 279.99, True, False, True, True, 15,
     "Premium pebbled leather with gold-tone hardware. Fits your essentials beautifully.", True),

    # Home & Living
    ("Artisan Coffee Maker", "Home & Living", 229.99, 169.99, False, True, True, True, 30,
     "Brew café-quality coffee at home. Temperature-controlled, bloom pre-infusion, stunning borosilicate carafe.", True),
    ("Egyptian Cotton Bedding Set", "Home & Living", 179.99, 129.99, True, True, False, True, 22,
     "1000-thread-count sateen weave. Cool, silky, and breathable for the perfect night's sleep.", True),
    ("Scented Soy Candle Collection", "Home & Living", 69.99, None, False, False, True, True, 100,
     "Set of 6 hand-poured soy candles. Slow-burning with premium fragrance oils. Zero toxins.", False),
    ("Monstera Planter Set", "Home & Living", 59.99, 44.99, False, True, True, False, 40,
     "Glazed ceramic with drainage holes. Set of 3 nesting sizes in a timeless matte finish.", False),

    # Beauty
    ("Vitamin C Brightening Serum", "Beauty", 89.99, 64.99, True, True, False, True, 55,
     "20% pure L-ascorbic acid with ferulic acid. Visibly brighter skin in 4 weeks, guaranteed.", True),
    ("Retinol Night Repair Cream", "Beauty", 119.99, 84.99, True, False, True, True, 38,
     "0.5% encapsulated retinol for maximum efficacy with minimal irritation. Wake up to smoother skin.", True),
    ("Luxury Perfume – Oud & Rose", "Beauty", 199.99, None, True, True, True, True, 20,
     "An opulent blend of Bulgarian rose and aged oud wood. Long-lasting 12+ hour sillage.", True),
    ("Hyaluronic Acid Moisturizer", "Beauty", 54.99, 39.99, False, True, True, False, 80,
     "Tri-weight hyaluronic acid complex. Plumps, hydrates, and protects skin barrier all day long.", False),

    # Sports
    ("Running Shoes Ultra Boost", "Sports", 179.99, 139.99, True, True, False, True, 35,
     "Carbon fibre plate for explosive energy return. Engineered mesh upper adapts to your foot shape.", True),
    ("Yoga Mat Premium Cork", "Sports", 89.99, 64.99, False, True, True, True, 45,
     "Natural cork surface grips better when wet. 5mm cushioning, 183cm length, carrying strap included.", False),
    ("Smart Jump Rope Digital", "Sports", 49.99, 34.99, False, False, True, False, 70,
     "LCD counter tracks jumps, calories, time. Adjustable cable, ball-bearing handles for smooth rotation.", False),

    # Gaming
    ("Gaming Controller Pro", "Gaming", 69.99, 54.99, False, True, True, True, 50,
     "Precision analog sticks with adjustable tension. Built-in rechargeable battery, 20-hour life.", True),
    ("Gaming Headset 7.1 Surround", "Gaming", 129.99, 89.99, True, True, False, True, 30,
     "Immersive virtual surround sound. Retractable noise-cancelling mic, plush memory foam ear cushions.", True),

    # Jewelry
    ("Gold Chain Necklace 18K", "Jewelry", 449.99, None, True, True, True, True, 8,
     "Solid 18-karat gold, 45cm length. Hallmarked and certified. Presented in a premium gift box.", True),
    ("Diamond Stud Earrings", "Jewelry", 799.99, 649.99, True, True, False, True, 5,
     "0.5ct total weight, VS1 clarity, G color. Set in 14K white gold with secure butterfly backs.", True),
]

REVIEW_TEXTS = [
    ("Absolutely love it!", "Exceeded all my expectations. Premium quality, fast delivery, packaged beautifully. Will definitely buy again!", 5),
    ("Great value for money", "Impressive build quality for the price point. Very happy with this purchase.", 4),
    ("Stunning quality", "The craftsmanship is exceptional. You can feel the difference compared to cheaper alternatives.", 5),
    ("Good but could be better", "Overall satisfied. Delivery was quick and the product matches the description well.", 4),
    ("Perfect gift!", "Bought this as a gift and the recipient absolutely loved it. Came in beautiful packaging.", 5),
    ("Highly recommend", "Third purchase from LuxeMart and every time the quality is outstanding. Loyal customer for life.", 5),
    ("Very impressed", "Better than the photos suggest. The attention to detail is remarkable.", 4),
    ("Worth every penny", "Premium product at a fair price. Customer service was also excellent when I had a question.", 5),
]

BANNERS = [
    ("Elevate Your Everyday", "New Season Collection 2025", "Discover premium products crafted for the modern lifestyle.", "Shop New Arrivals", "New Collection 2025"),
    ("Summer Style Edit", "Up to 40% Off Selected Items", "Refresh your wardrobe with our curated summer collection.", "Shop the Sale", "Limited Time Offer"),
    ("Tech That Inspires", "The Latest in Consumer Electronics", "Experience innovation with our handpicked tech selection.", "Explore Tech", "New Arrivals"),
]


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO('🌱 Seeding LuxeMart demo data...'))

        # Superuser
        if not User.objects.filter(email='admin@luxemart.com').exists():
            User.objects.create_superuser(
                username='admin', email='admin@luxemart.com',
                password='Admin@1234', first_name='Admin', last_name='LuxeMart'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser: admin@luxemart.com / Admin@1234'))

        # Demo users
        for i in range(1, 5):
            email = f'user{i}@luxemart.com'
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    username=f'user{i}', email=email, password='User@1234',
                    first_name=f'Demo', last_name=f'User{i}'
                )
        self.stdout.write(self.style.SUCCESS('✅ Demo users created'))

        # Brands
        brands = {}
        for name in BRANDS:
            b, _ = Brand.objects.get_or_create(name=name, defaults={'is_active': True})
            brands[name] = b
        self.stdout.write(self.style.SUCCESS(f'✅ {len(brands)} brands created'))

        # Categories
        cats = {}
        for name, icon, desc in CATEGORIES:
            c, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon, 'description': desc, 'is_active': True})
            cats[name] = c
        self.stdout.write(self.style.SUCCESS(f'✅ {len(cats)} categories created'))

        # Products
        product_list = []
        for i, item in enumerate(PRODUCTS):
            (name, cat_name, price, disc_price, featured, trending, best_seller, new_arrival, stock, desc, is_new) = item
            cat = cats.get(cat_name)
            if not cat:
                continue
            brand = random.choice(list(brands.values()))
            p, created = Product.objects.get_or_create(
                name=name,
                defaults=dict(
                    category=cat, brand=brand, price=price,
                    discount_price=disc_price, description=desc,
                    short_description=desc[:150],
                    stock_quantity=stock, is_active=True,
                    is_featured=featured, is_trending=trending,
                    is_best_seller=best_seller, is_new_arrival=new_arrival,
                    specifications={
                        "Brand": brand.name, "Category": cat_name,
                        "Warranty": "1 Year", "In Box": "Product + Manual + Warranty Card"
                    }
                )
            )
            product_list.append(p)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(product_list)} products created'))

        # Reviews
        users = list(User.objects.all())
        review_count = 0
        for p in product_list[:15]:
            sample_users = random.sample(users, min(3, len(users)))
            for u in sample_users:
                r_data = random.choice(REVIEW_TEXTS)
                Review.objects.get_or_create(
                    product=p, user=u,
                    defaults=dict(title=r_data[0], body=r_data[1], rating=r_data[2], is_approved=True)
                )
                review_count += 1
        self.stdout.write(self.style.SUCCESS(f'✅ {review_count} reviews created'))

        # Banners
        for i, (title, subtitle, desc, cta, badge) in enumerate(BANNERS):
            Banner.objects.get_or_create(
                title=title,
                defaults=dict(subtitle=subtitle, description=desc, cta_text=cta, badge_text=badge, is_active=True, order=i)
            )
        self.stdout.write(self.style.SUCCESS(f'✅ {len(BANNERS)} banners created'))

        # Coupons
        for code, disc_type, val in [('WELCOME10', 'percentage', 10), ('LUXE20', 'percentage', 20), ('FLAT25', 'fixed', 25)]:
            Coupon.objects.get_or_create(code=code, defaults=dict(discount_type=disc_type, discount_value=val, is_active=True, minimum_order=50))
        self.stdout.write(self.style.SUCCESS('✅ Coupons: WELCOME10, LUXE20, FLAT25'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write(self.style.HTTP_INFO('Admin: http://127.0.0.1:8000/admin  |  admin@luxemart.com / Admin@1234'))
        self.stdout.write(self.style.HTTP_INFO('Run: python manage.py runserver'))

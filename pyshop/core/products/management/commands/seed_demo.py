from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import CartItem, Category, OrderItem, Product, Review, Wishlist


DEMO_PRODUCTS = [
    {
        "category": "Workspace",
        "name": "Auralux Wireless Desk Speaker",
        "price": Decimal("7499.00"),
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=1200&q=80",
        "description": "A compact wireless speaker with crisp audio, soft-touch controls, and a premium aluminum body for focused work sessions.",
    },
    {
        "category": "Workspace",
        "name": "Orbit Mechanical Keyboard",
        "price": Decimal("5999.00"),
        "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=1200&q=80",
        "description": "Hot-swappable switches, clean keycaps, and a quiet typing profile built for developers, designers, and creators.",
    },
    {
        "category": "Travel",
        "name": "Nomad Pro Carry Backpack",
        "price": Decimal("4299.00"),
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=80",
        "description": "Weather-resistant daily backpack with laptop protection, hidden pockets, and a structured silhouette for commuting.",
    },
    {
        "category": "Lifestyle",
        "name": "PulseFit Smart Watch",
        "price": Decimal("8999.00"),
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=80",
        "description": "A polished fitness watch with health metrics, long battery life, and a minimal interface for everyday tracking.",
    },
    {
        "category": "Creator Gear",
        "name": "Lumina 4K Creator Camera",
        "price": Decimal("38999.00"),
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1200&q=80",
        "description": "Portable 4K camera with fast autofocus, cinematic color, and creator-friendly controls for product and travel content.",
    },
    {
        "category": "Lifestyle",
        "name": "CalmBrew Ceramic Set",
        "price": Decimal("2199.00"),
        "image_url": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=1200&q=80",
        "description": "Minimal ceramic pour-over set for slow mornings, clean kitchen counters, and elevated daily rituals.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with a polished demo catalog for screenshots and portfolio reviews."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Remove existing catalog and product-linked records before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            CartItem.objects.all().delete()
            OrderItem.objects.all().delete()
            Wishlist.objects.all().delete()
            Review.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()

        created = 0

        for item in DEMO_PRODUCTS:
            category, _ = Category.objects.get_or_create(name=item["category"])
            _, was_created = Product.objects.update_or_create(
                name=item["name"],
                defaults={
                    "category": category,
                    "price": item["price"],
                    "image_url": item["image_url"],
                    "description": item["description"],
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Demo catalog ready. {created} new products created."))

from django.core.management.base import BaseCommand
from djangoapp.models import Dealer

DEALERS = [
    {"name": "Metro Auto Center", "city": "Austin", "state": "TX", "address": "100 Congress Ave", "zip_code": "78701"},
    {"name": "Lakeside Motors", "city": "Dallas", "state": "TX", "address": "250 Main Street", "zip_code": "75201"},
    {"name": "Golden Gate Cars", "city": "San Francisco", "state": "CA", "address": "75 Market Street", "zip_code": "94105"},
    {"name": "Empire State Auto", "city": "New York", "state": "NY", "address": "10 Broadway", "zip_code": "10004"},
]

class Command(BaseCommand):
    help = "Create a small set of clearly marked demo dealerships for local testing."

    def handle(self, *args, **options):
        created = 0
        for data in DEALERS:
            _, was_created = Dealer.objects.get_or_create(name=data["name"], defaults=data)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created} demo dealers created."))

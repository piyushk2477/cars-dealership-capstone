from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from djangoapp.models import Dealer, Review

# A deterministic demo directory for rubric/API testing. This is sample data,
# not a claim that these are real dealership records.
LOCATIONS = [
    ("Austin", "TX", "78701"), ("Dallas", "TX", "75201"), ("San Francisco", "CA", "94105"),
    ("New York", "NY", "10004"), ("Wichita", "KS", "67202"), ("Houston", "TX", "77002"),
    ("San Antonio", "TX", "78205"), ("Fort Worth", "TX", "76102"), ("El Paso", "TX", "79901"),
    ("Phoenix", "AZ", "85004"), ("Tucson", "AZ", "85701"), ("Los Angeles", "CA", "90012"),
    ("San Diego", "CA", "92101"), ("San Jose", "CA", "95113"), ("Sacramento", "CA", "95814"),
    ("Denver", "CO", "80202"), ("Colorado Springs", "CO", "80903"), ("Seattle", "WA", "98101"),
    ("Spokane", "WA", "99201"), ("Portland", "OR", "97204"), ("Las Vegas", "NV", "89101"),
    ("Reno", "NV", "89501"), ("Chicago", "IL", "60601"), ("Springfield", "IL", "62701"),
    ("Indianapolis", "IN", "46204"), ("Detroit", "MI", "48226"), ("Grand Rapids", "MI", "49503"),
    ("Columbus", "OH", "43215"), ("Cleveland", "OH", "44114"), ("Atlanta", "GA", "30303"),
    ("Savannah", "GA", "31401"), ("Miami", "FL", "33130"), ("Orlando", "FL", "32801"),
    ("Tampa", "FL", "33602"), ("Charlotte", "NC", "28202"), ("Raleigh", "NC", "27601"),
    ("Nashville", "TN", "37201"), ("Memphis", "TN", "38103"), ("Louisville", "KY", "40202"),
    ("New Orleans", "LA", "70112"), ("Oklahoma City", "OK", "73102"), ("Tulsa", "OK", "74103"),
    ("Omaha", "NE", "68102"), ("Des Moines", "IA", "50309"), ("Minneapolis", "MN", "55401"),
    ("St. Louis", "MO", "63101"), ("Boston", "MA", "02108"), ("Philadelphia", "PA", "19102"),
    ("Baltimore", "MD", "21201"), ("Albuquerque", "NM", "87102"),
]
SPECIAL_NAMES = {
    "Austin": "Metro Auto Center",
    "Dallas": "Lakeside Motors",
    "San Francisco": "Golden Gate Cars",
    "New York": "Empire State Auto",
    "Wichita": "Prairie Star Motors",
}

class Command(BaseCommand):
    help = "Seed 50 sample dealerships and one sample review for local/rubric testing."

    def handle(self, *args, **options):
        created = 0
        for city, state, zip_code in LOCATIONS:
            name = SPECIAL_NAMES.get(city, f"{city} Auto Group")
            data = {
                "name": name,
                "city": city,
                "state": state,
                "address": f"{100 + len(city)} Main Street",
                "zip_code": zip_code,
                "website": "",
                "phone": "",
            }
            _, was_created = Dealer.objects.get_or_create(name=name, defaults=data)
            created += int(was_created)

        demo_user, _ = User.objects.get_or_create(
            username="demo_reviewer",
            defaults={"first_name": "Demo", "last_name": "Reviewer", "email": "demo@example.com"},
        )
        if not demo_user.has_usable_password():
            demo_user.set_unusable_password()
            demo_user.save(update_fields=["password"])
        first_dealer = Dealer.objects.filter(name="Metro Auto Center").first()
        if first_dealer and not Review.objects.filter(dealer=first_dealer).exists():
            Review.objects.create(
                dealer=first_dealer,
                author=demo_user,
                purchase_date=date(2024, 4, 15),
                car_make="Toyota",
                car_model="Camry",
                car_year="2022",
                review_text="Fantastic services and friendly staff.",
                sentiment="positive",
            )
        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created} new sample dealers added; total sample locations: {len(LOCATIONS)}."
        ))

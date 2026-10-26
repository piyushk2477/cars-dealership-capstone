from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Dealer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("state", models.CharField(db_index=True, max_length=2)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("zip_code", models.CharField(blank=True, max_length=12)),
                ("website", models.URLField(blank=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("car_make", models.CharField(blank=True, max_length=80)),
                ("car_model", models.CharField(blank=True, max_length=80)),
                ("review_text", models.TextField()),
                ("sentiment", models.CharField(blank=True, max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="dealer_reviews", to=settings.AUTH_USER_MODEL)),
                ("dealer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="djangoapp.dealer")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

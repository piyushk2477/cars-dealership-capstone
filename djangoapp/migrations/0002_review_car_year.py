from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("djangoapp", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="review",
            name="car_year",
            field=models.CharField(blank=True, max_length=4),
        ),
    ]

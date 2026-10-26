from django.conf import settings
from django.db import models

class Dealer(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, db_index=True)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dealer_reviews")
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=80, blank=True)
    car_model = models.CharField(max_length=80, blank=True)
    car_year = models.CharField(max_length=4, blank=True)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review for {self.dealer} by {self.author}"

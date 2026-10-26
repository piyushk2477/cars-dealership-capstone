from django.contrib import admin
from .models import Dealer, Review

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state")
    search_fields = ("name", "city", "state")
    list_filter = ("state",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("dealer", "author", "sentiment", "created_at")
    list_filter = ("sentiment", "created_at")

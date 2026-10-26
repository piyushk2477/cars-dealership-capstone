from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from djangoapp import views as api_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    path("fetchDealers", api_views.legacy_fetch_dealers, name="legacy_fetch_dealers"),
    path("fetchDealers/<str:state>", api_views.legacy_fetch_dealers, name="legacy_fetch_dealers_by_state"),
    path("fetchDealer/<int:dealer_id>", api_views.legacy_fetch_dealer, name="legacy_fetch_dealer"),
    path("fetchReviews/dealer/<int:dealer_id>", api_views.legacy_fetch_reviews, name="legacy_fetch_reviews"),
    path("analyze/<path:text>", api_views.legacy_analyze, name="legacy_analyze"),
    path("login", api_views.legacy_login, name="legacy_login"),
    path("logout", api_views.logout_user, name="legacy_logout"),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
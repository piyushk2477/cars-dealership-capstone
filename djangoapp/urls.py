from django.urls import path
from . import views

urlpatterns = [
    path("get_dealers", views.get_dealers, name="get_dealers"),
    path("get_dealer_by_id/<int:dealer_id>", views.get_dealer_by_id, name="get_dealer_by_id"),
    path("get_dealer_reviews/<int:dealer_id>", views.get_dealer_reviews, name="get_dealer_reviews"),
    path("get_dealers_by_state/<str:state>", views.get_dealers_by_state, name="get_dealers_by_state"),
    path("get_cars", views.get_cars, name="get_cars"),
    path("get_all_car_makes", views.get_all_car_makes, name="get_all_car_makes"),
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("add_review", views.add_review, name="add_review"),
    path("analyze_review", views.analyze_review, name="analyze_review"),
]
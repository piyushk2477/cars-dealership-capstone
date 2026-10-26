import json
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import Dealer, Review

def _body(request):
    try:
        return json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}

def _dealer_dict(dealer):
    return {
        "id": dealer.id, "name": dealer.name, "city": dealer.city,
        "state": dealer.state, "address": dealer.address,
        "zip": dealer.zip_code, "website": dealer.website, "phone": dealer.phone,
    }

@require_GET
def get_dealers(request):
    dealers = Dealer.objects.all().order_by("name")
    state = request.GET.get("state")
    if state:
        dealers = dealers.filter(state__iexact=state.strip())
    return JsonResponse({"dealers": [_dealer_dict(d) for d in dealers]})

@require_GET
def get_dealer_by_id(request, dealer_id):
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)
    return JsonResponse({"dealer": _dealer_dict(dealer)})

@require_GET
def get_dealer_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id).select_related("author", "dealer")
    data = [{
        "id": r.id, "dealer_id": r.dealer_id, "dealer_name": r.dealer.name,
        "name": r.author.get_full_name() or r.author.username,
        "review": r.review_text, "review_text": r.review_text,
        "sentiment": r.sentiment, "car_make": r.car_make, "car_model": r.car_model,
        "purchase_date": r.purchase_date.isoformat() if r.purchase_date else None,
        "created_at": r.created_at.isoformat(),
    } for r in reviews]
    return JsonResponse({"reviews": data})

@require_GET
def get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state.strip()).order_by("name")
    return JsonResponse({"dealers": [_dealer_dict(d) for d in dealers], "state": state.upper()})

@require_GET
def get_cars(request):
    # Replace this starter list with the course-provided inventory dataset when available.
    return JsonResponse({"cars": [
        {"id": 1, "make": "Toyota", "model": "Camry", "year": 2024},
        {"id": 2, "make": "Honda", "model": "Civic", "year": 2024},
        {"id": 3, "make": "Ford", "model": "Mustang", "year": 2023},
    ]})

@require_GET
def get_all_car_makes(request):
    """Return the unique car makes available in the starter inventory."""
    makes = sorted({car["make"] for car in [
        {"make": "Toyota"}, {"make": "Honda"}, {"make": "Ford"}
    ]})
    return JsonResponse({"car_makes": makes})

@csrf_exempt
@require_POST
def register_user(request):
    data = _body(request)
    username, password = data.get("username", "").strip(), data.get("password", "")
    email = data.get("email", "").strip()
    if not username or not password or not email:
        return JsonResponse({"error": "username, email, and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=409)
    user = User.objects.create_user(username=username, password=password, email=email)
    return JsonResponse({"message": "Registration successful", "user": {"id": user.id, "username": user.username}}, status=201)

@csrf_exempt
@require_POST
def login_user(request):
    data = _body(request)
    user = authenticate(request, username=data.get("username", ""), password=data.get("password", ""))
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)
    login(request, user)
    return JsonResponse({"message": "Login successful", "user": {"id": user.id, "username": user.username}})

@csrf_exempt
@require_POST
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})

@csrf_exempt
@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required to submit a review"}, status=401)
    data = _body(request)
    dealer_id, review_text = data.get("dealer_id"), data.get("review") or data.get("review_text", "")
    if not dealer_id or not str(review_text).strip():
        return JsonResponse({"error": "dealer_id and review text are required"}, status=400)
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except (Dealer.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"error": "Dealer not found"}, status=404)
    purchase_date = None
    if data.get("purchase_date"):
        try:
            purchase_date = date.fromisoformat(data["purchase_date"])
        except (ValueError, TypeError):
            return JsonResponse({"error": "purchase_date must use YYYY-MM-DD"}, status=400)
    review = Review.objects.create(
        dealer=dealer, author=request.user, review_text=str(review_text).strip(),
        car_make=data.get("car_make", ""), car_model=data.get("car_model", ""),
        purchase_date=purchase_date, sentiment=_sentiment(str(review_text)),
    )
    return JsonResponse({"message": "Review added", "review_id": review.id, "sentiment": review.sentiment}, status=201)

def _sentiment(text):
    positive = {"great", "excellent", "helpful", "friendly", "love", "good", "amazing", "recommend"}
    negative = {"bad", "poor", "rude", "awful", "terrible", "hate", "waste", "disappointing"}
    words = {word.strip(".,!?;:").lower() for word in text.split()}
    score = len(words & positive) - len(words & negative)
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"

@csrf_exempt
@require_POST
def analyze_review(request):
    data = _body(request)
    text = str(data.get("review", data.get("review_text", ""))).strip()
    if not text:
        return JsonResponse({"error": "review text is required"}, status=400)
    return JsonResponse({"review": text, "sentiment": _sentiment(text)})

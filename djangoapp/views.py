import json
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import Dealer, Review

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}
STATE_CENTERS = {
    "CA": (36.7783, -119.4179), "KS": (38.5, -98.0), "TX": (31.0, -99.0),
    "NY": (42.9, -75.5), "IL": (40.0, -89.0), "FL": (27.8, -81.7),
    "CO": (39.0, -105.5), "WA": (47.4, -120.7), "AZ": (34.2, -111.7),
}

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

def _legacy_dealer_dict(dealer):
    lat, long = STATE_CENTERS.get(dealer.state, (39.5, -98.35))
    # These coordinates are demo approximations for this learning project.
    return {
        "_id": str(dealer.id), "id": dealer.id, "city": dealer.city,
        "state": STATE_NAMES.get(dealer.state, dealer.state),
        "address": dealer.address, "zip": dealer.zip_code,
        "lat": round(lat + (dealer.id % 7) * 0.01, 6),
        "long": round(long + (dealer.id % 7) * 0.01, 6),
        "short_name": dealer.name, "full_name": dealer.name, "__v": 0,
    }

@require_GET
def get_dealers(request):
    dealers = Dealer.objects.all().order_by("id")
    state = request.GET.get("state")
    if state:
        code = next((abbr for abbr, name in STATE_NAMES.items() if name.lower() == state.strip().lower()), state.strip())
        dealers = dealers.filter(state__iexact=code)
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
        "dealership": r.dealer.name, "review": r.review_text,
        "review_text": r.review_text, "sentiment": r.sentiment,
        "purchase": bool(r.purchase_date), "purchase_date": r.purchase_date.isoformat() if r.purchase_date else None,
        "car_make": r.car_make, "car_model": r.car_model, "car_year": getattr(r, "car_year", ""),
        "created_at": r.created_at.isoformat(),
    } for r in reviews]
    return JsonResponse({"reviews": data})

@require_GET
def get_dealers_by_state(request, state):
    code = next((abbr for abbr, name in STATE_NAMES.items() if name.lower() == state.strip().lower()), state.strip())
    dealers = Dealer.objects.filter(state__iexact=code).order_by("id")
    return JsonResponse({"dealers": [_dealer_dict(d) for d in dealers], "state": state.upper()})

CAR_MODELS = [
    {"CarModel": "Pathfinder", "CarMake": "NISSAN"},
    {"CarModel": "Qashqai", "CarMake": "NISSAN"},
    {"CarModel": "XTRAIL", "CarMake": "NISSAN"},
    {"CarModel": "A-Class", "CarMake": "Mercedes"},
    {"CarModel": "C-Class", "CarMake": "Mercedes"},
    {"CarModel": "E-Class", "CarMake": "Mercedes"},
    {"CarModel": "A4", "CarMake": "Audi"},
    {"CarModel": "A5", "CarMake": "Audi"},
    {"CarModel": "A6", "CarMake": "Audi"},
    {"CarModel": "Sorrento", "CarMake": "Kia"},
    {"CarModel": "Carnival", "CarMake": "Kia"},
    {"CarModel": "Cerato", "CarMake": "Kia"},
    {"CarModel": "Corolla", "CarMake": "Toyota"},
    {"CarModel": "Camry", "CarMake": "Toyota"},
    {"CarModel": "Kluger", "CarMake": "Toyota"},
]

@require_GET
def get_cars(request):
    return JsonResponse({
        "CarModels": CAR_MODELS,
        "cars": [{"id": i + 1, "make": item["CarMake"], "model": item["CarModel"], "year": 2024}
                 for i, item in enumerate(CAR_MODELS)],
    })

@require_GET
def get_all_car_makes(request):
    return JsonResponse({"car_makes": sorted({car["CarMake"] for car in CAR_MODELS})})

@csrf_exempt
@require_POST
def register_user(request):
    data = _body(request)
    username = str(data.get("username", data.get("userName", ""))).strip()
    password = data.get("password", data.get("Password", ""))
    email = str(data.get("email", "")).strip()
    if not username or not password or not email:
        return JsonResponse({"error": "username, email, and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=409)
    user = User.objects.create_user(username=username, password=password, email=email, first_name=str(data.get("first_name", data.get("firstName", ""))).strip(), last_name=str(data.get("last_name", data.get("lastName", ""))).strip())
    return JsonResponse({"message": "Registration successful", "user": {"id": user.id, "username": user.username}}, status=201)

@csrf_exempt
@require_POST
def login_user(request):
    data = _body(request)
    username = data.get("userName", data.get("username", ""))
    password = data.get("password", data.get("Password", ""))
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)
    login(request, user)
    return JsonResponse({"message": "Login successful", "user": {"id": user.id, "username": user.username}, "userName": user.username, "status": "Authenticated"})

@csrf_exempt
def logout_user(request):
    if request.method not in ("GET", "POST"):
        return JsonResponse({"error": "Use GET or POST"}, status=405)
    logout(request)
    if request.path == "/logout":
        return JsonResponse({"userName": ""})
    return JsonResponse({"message": "Logout successful", "userName": ""})

@csrf_exempt
@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required to submit a review"}, status=401)
    data = _body(request)
    dealer_id = data.get("dealer_id", data.get("dealership"))
    review_text = data.get("review") or data.get("review_text", "")
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
        car_year=str(data.get("car_year", "")), purchase_date=purchase_date,
        sentiment=_sentiment(str(review_text)),
    )
    return JsonResponse({"message": "Review added", "review_id": review.id, "sentiment": review.sentiment}, status=201)

def _sentiment(text):
    positive = {"great", "excellent", "helpful", "friendly", "love", "good", "amazing", "recommend", "fantastic", "services", "service", "wonderful", "awesome"}
    negative = {"bad", "poor", "rude", "awful", "terrible", "hate", "waste", "disappointing", "horrible"}
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

@require_GET
def legacy_fetch_dealers(request, state=None):
    dealers = Dealer.objects.all().order_by("id")
    if state:
        code = next((abbr for abbr, name in STATE_NAMES.items() if name.lower() == state.strip().lower()), state.strip())
        dealers = dealers.filter(state__iexact=code)
    return JsonResponse([_legacy_dealer_dict(d) for d in dealers], safe=False)

@require_GET
def legacy_fetch_dealer(request, dealer_id):
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)
    return JsonResponse(_legacy_dealer_dict(dealer))

@require_GET
def legacy_fetch_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id).select_related("author", "dealer")
    return JsonResponse([{
        "name": r.author.get_full_name() or r.author.username,
        "dealership": r.dealer.name, "review": r.review_text,
        "purchase": bool(r.purchase_date),
        "purchase_date": r.purchase_date.isoformat() if r.purchase_date else "",
        "car_make": r.car_make, "car_model": r.car_model,
        "car_year": getattr(r, "car_year", ""),
    } for r in reviews], safe=False)

@require_GET
def legacy_analyze(request, text):
    return JsonResponse({"sentiment": _sentiment(text)})

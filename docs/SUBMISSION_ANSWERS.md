# Capstone Resubmission Answers

Use these entries for the 28-task capstone resubmission. Run the commands against the updated project first. Do not paste illustrative JSON in place of actual command output; for list endpoints, copy the full output printed by your own server.

## Before collecting evidence

From the repository root, run:

```powershell
python manage.py migrate --noinput
python manage.py seed_dealers
python manage.py runserver
```

In a second terminal, test API endpoints with the commands below. The seed command creates 50 **sample/demo** dealership records and a sample review; coordinates are demo approximations, not verified dealership coordinates.

## Task 1 — README URL

Public README URL:
https://github.com/piyushk2477/cars-dealership-capstone/blob/main/README.md

Project name: `fullstack_developer_capstone`  
Repository name: `cars-dealership-capstone`

Note: the exact requested repository name `xrwvm-fullstack_developer_capstone` was unavailable, so this project remains in the existing repository.

## Task 2 — Django server output

The previously submitted server output received full credit. Keep it if the app still starts successfully. Otherwise run `python manage.py runserver` and paste the real terminal output showing system checks passed and the local server URL.

## Task 3 — About Us page URL

https://github.com/piyushk2477/cars-dealership-capstone/blob/main/server/frontend/static/About.html

## Task 4 — Contact Us page URL

https://github.com/piyushk2477/cars-dealership-capstone/blob/main/server/frontend/static/Contact.html

## Task 5 — Login request and output

Make sure the user exists first. If needed, register a new user using the updated endpoint:

```powershell
curl.exe -X POST http://127.0.0.1:8000/djangoapp/register -H "Content-Type: application/json" -d "{\"username\":\"capstoneuser\",\"first_name\":\"Capstone\",\"last_name\":\"User\",\"email\":\"capstoneuser@example.com\",\"password\":\"CapstonePass123!\"}"
```

Then paste this command and its real output:

```powershell
curl.exe -X POST http://127.0.0.1:8000/djangoapp/login -H "Content-Type: application/json" -d "{\"userName\":\"capstoneuser\",\"password\":\"CapstonePass123!\"}"
```

Expected JSON for a successful login:

```json
{"userName":"capstoneuser","status":"Authenticated"}
```

## Task 6 — Logout request and output

```powershell
curl.exe -X GET http://127.0.0.1:8000/djangoapp/logout
```

Expected JSON:

```json
{"userName":""}
```

## Task 7 — Register component URL

https://github.com/piyushk2477/cars-dealership-capstone/blob/main/server/frontend/src/components/Register/Register.jsx

## Task 8 — Reviews for dealer ID 1

```powershell
curl.exe http://127.0.0.1:8000/fetchReviews/dealer/1
```

After running `python manage.py seed_dealers`, the seeded first dealer should have a sample review. Paste the full JSON returned by your server. It includes reviewer name, dealer ID, review text, purchase flag/date, and car make/model/year.

## Task 9 — All 50 dealers

```powershell
curl.exe http://127.0.0.1:8000/fetchDealers
```

Paste the complete output array (all 50 records). Each record contains `_id`, `id`, `city`, `state`, `address`, `zip`, `lat`, `long`, `short_name`, `full_name`, and `__v`.

## Task 10 — Dealer details by ID

```powershell
curl.exe http://127.0.0.1:8000/fetchDealer/1
```

Paste the complete JSON output. It includes the required dealer ID, city, state, address, ZIP, latitude, longitude, short name, and full name.

## Task 11 — Dealers in Kansas

```powershell
curl.exe http://127.0.0.1:8000/fetchDealers/Kansas
```

Paste the complete JSON output showing the Kansas record(s) and all required fields.

## Task 12 — Admin login screenshot

Previously received full credit. Keep the existing `admin_login.png` screenshot if it remains valid.

## Task 13 — Admin logout screenshot

Previously received full credit. Keep the existing `admin_logout.png` screenshot if it remains valid.

## Tasks 14–15 — Car makes and models

```powershell
curl.exe http://127.0.0.1:8000/djangoapp/get_cars
```

Expected response shape: a JSON object containing a `CarModels` array with 15 `CarModel` / `CarMake` pairs. Paste the full output from the running server.

## Task 16 — Sentiment analysis

```powershell
curl.exe --path-as-is http://127.0.0.1:8000/analyze/Fantastic%20services
```

Expected JSON:

```json
{"sentiment":"positive"}
```

## Task 17 — Home page before login

Keep the previously accepted `get_dealers.png` screenshot if it still matches the current UI. Otherwise capture the dealer list before logging in, with the browser address bar visible.

## Task 18 — Home page after login

Capture `get_dealers_loggedin.png` after signing in. Make sure the screenshot visibly includes the actual username, dealer list, Review Dealer/review option, and browser address bar.

## Task 19 — Filter by state

Keep the previously accepted `dealersbystate.png` screenshot if still valid. It should show the filtered list and browser address bar.

## Task 20 — Dealer detail and reviews

Keep the previously accepted `dealer_id_reviews.png` screenshot if still valid. It should show the selected dealer, review(s), and browser address bar.

## Task 21 — Review form before submission

Capture `dealership_review_submission.png` after filling in review text, purchase date, car make, car model, and car year, with the **Post Review** button visible. Do not submit the form before taking this screenshot.

## Task 22 — Posted review

Keep the previously accepted `added_review.png` screenshot if it still shows the submitted review and sentiment label.

## Task 23 — CI/CD output

GitHub Actions run page:
https://github.com/piyushk2477/cars-dealership-capstone/actions

The workflow now has jobs named **Lint Python Files**, **Lint JavaScript Files**, and **Django tests**. Open the latest successful run and copy the actual job/step output. Do not reuse an older run that only showed a single test job.

## Task 24 — Public deployment URL

This cannot be filled until the application is actually deployed. Paste the real public URL after deployment, for example the URL assigned by your chosen hosting provider. Do not submit localhost as a public deployment URL.

## Task 25 — Deployed landing page screenshot

After deployment, capture the real public landing page as `deployed_landingpage.png`.

## Task 26 — Deployed logged-in screenshot

After deployment, sign in and capture `deployed_loggedin.png`, showing the logged-in username and dealer list.

## Task 27 — Deployed dealer detail screenshot

After deployment, open a dealer detail/reviews view and capture `deployed_dealer_detail.png`.

## Task 28 — Deployed review screenshot

After deployment, submit a review and capture `deployed_add_review.png`, showing the posted review and sentiment result.

**Important:** Tasks 24–28 require a real deployment and genuine screenshots. They cannot be truthfully completed by writing a sample URL or generating mock evidence.

# PocketSmart AI

FastAPI + Jinja2 + SQLite + Gemini budget/recommendation assistant.

The supplied documentation describes Home, Party and Jewelry planners, authentication,
history, optional jewelry image input, Gemini integration and marketplace-oriented
recommendations. This implementation includes those features.

The documentation names Gemini 1.5 Flash Pro. The code uses the current Google GenAI
Python SDK and a configurable `GEMINI_MODEL`, defaulting to `gemini-2.5-flash`.
Change the value in `.env` if you have access to another supported model.

Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO are represented by a local demo catalog rather
than scraped live data. This keeps the project runnable without private marketplace
credentials and prevents fabricated live prices.

## Windows / VS Code

```powershell
cd PocketSmartAI
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Put your Gemini API key in `.env`:

`GEMINI_API_KEY=your_key_here`

If the key is empty or Gemini is unavailable, the app uses a safe local demo fallback.

Run:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Test:

```powershell
pytest -q
```

## Structure

```text
PocketSmartAI/
  app/
    main.py config.py database.py models.py schemas.py auth.py catalog.py ai_service.py
    routes/web.py routes/api.py
    services/recommendation_service.py
    templates/
    static/css/style.css
    static/js/app.js
  tests/test_app.py
  requirements.txt
  .env.example
  README.md
```

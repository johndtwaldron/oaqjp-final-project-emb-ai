# IBM – Developing AI Applications with Python & Flask
## Module 1 Living Notes (JDW ₿ | Bitvocation CV Doctor)

Purpose: capture **osmosis-mode** notes you can reuse across solo + professional projects (e.g., Bitvocation CV Doctor: Python + Flask + Vercel). Keep this as a living doc and append as you go.

---

## 0) TL;DR for Module 1
- **Web App vs API**: Web app renders UI (HTML/CSS/JS) while an API exposes **data/services** (usually JSON). All web apps **use** APIs; not all APIs are web apps.
- **Lifecycle**: Requirements → Analysis → Design → Code & Unit Tests → User/System/Performance Tests → Production → Maintenance.
- **PEP 8**: readable code, consistent naming, 4‑space indentation, spaces around ops, blank lines around defs/classes.
- **Static Analysis**: run linters/formatters without executing the code (e.g., `pylint`, `flake8`, `black`, `isort`).
- **Unit Testing**: fast checks for functions/classes; run locally and in CI.
- **Modules & Packages**: structure code across files, create `__init__.py`, and verify imports.

---

## 1) Web Applications vs APIs
**Web App**  
- Responsibilities: routing, templates, forms, sessions, cookies, auth, server‑side rendering.  
- Example UI route:
```python
@app.get("/")
def home():
    return render_template("index.html")
```

**API**  
- Responsibilities: machine‑consumable endpoints, JSON/XML responses, versioning, idempotency, auth tokens.  
- Example JSON route:
```python
from flask import jsonify

@app.get("/api/v1/healthz")
def healthz():
    return jsonify(status="ok"), 200
```

**Typical clients**  
- Web app: browsers.  
- API: browsers, CLIs, mobile apps, webhooks, other services.

**CV‑Doctor tie‑in**  
- API endpoints for **document upload**, **CV parse**, **score**, **export**; web app for dashboards and human review.

---

## 2) Application Development Lifecycle (pragmatic view)
1. **Requirements** – user stories, success criteria, non‑functionals (perf, security, compliance).
2. **Analysis** – feasibility, risks, data flow, systems impacted.
3. **Design** – API schema, DB schema, component boundaries, error contracts, logging model.
4. **Code + Unit Tests** – TDD where feasible; keep functions small; document edge cases.
5. **User/System/Perf Tests** – usability, integrations, load/stress; traceability back to reqs.
6. **Production** – containerization, env configs, secrets, observability (logs/metrics/traces).
7. **Maintenance** – patching, upgrades, incident response, SLOs/SLIs, backlog grooming.

**Artifacts to keep**  
- ADRs (Architecture Decision Records), OpenAPI spec, Makefile, CI workflow, `pyproject.toml`, `README.md`, `CONTRIBUTING.md`.

---

## 3) Clean Code & PEP 8 Essentials
- 4 spaces (no tabs).  
- 79–88 char line length (PEP 8 says 79; *Black* defaults to 88).  
- Blank lines around top‑level defs/classes; spaces around operators/after commas.
- Naming:
  - functions/files: `lower_snake_case`
  - classes: `CamelCase`
  - constants: `UPPER_SNAKE_CASE`
- Put bigger logic chunks **inside** functions/classes (not top‑level script code).
- Prefer pure functions and narrow interfaces.

**Example**
```python
MAX_FILE_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

def score_cv(tokens: list[str]) -> float:
    '''Return a 0..1 score based on token features.'''
    weight = sum(1 for t in tokens if t.lower() in {'python', 'flask', 'pytest'})
    return min(weight / 10.0, 1.0)
```

---

## 4) Static Code Analysis & Formatting
Run without executing the app.

### Tools
- **pylint** – style & code smells
- **flake8** – style + simple linting
- **black** – opinionated auto‑formatter
- **isort** – import sorting
- **mypy** (opt) – static type checker

### Install (dev)
```bash
pip install pylint flake8 black isort mypy
```

### Recommended `pyproject.toml` snippet
```toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.isort]
profile = "black"

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203","W503"]
```

### Usage
```bash
black .
isort .
flake8
pylint src  # or your package path
mypy src    # if using type hints
```

**Pre-commit (nice-to-have)**
```bash
pip install pre-commit
pre-commit install
```
`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks: [{ id: black }]
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks: [{ id: isort }]
  - repo: https://github.com/PyCQA/flake8
    rev: 7.1.1
    hooks: [{ id: flake8 }]
```

---

## 5) Unit Testing (unittest & pytest)
**unittest example**
```python
# tests/test_mathutils.py
import unittest
from mypkg.mathutils import add

class TestMathUtils(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()
```

**pytest example (preferred)**
```python
# tests/test_mathutils_pytest.py
from mypkg.mathutils import add
import pytest

@pytest.mark.parametrize("a,b,exp", [(2,3,5), (0,0,0), (-1,1,0)])
def test_add(a, b, exp):
    assert add(a, b) == exp
```

**Run**
```bash
pytest -q
```

**What to test**
- Happy path + edge cases (empty input, None, out‑of‑range, invalid types).
- Error messages & HTTP status codes (for Flask routes).
- Pure functions first; then adapters (file, DB, HTTP).

---

## 6) Modules & Packages (structuring code)
**Minimal package layout**
```
project-root/
  pyproject.toml
  src/mypkg/__init__.py
  src/mypkg/mathutils.py
  tests/
```

**`src/mypkg/mathutils.py`**
```python
def add(a: int, b: int) -> int:
    return a + b
```

**`src/mypkg/__init__.py`**
```python
from .mathutils import add
__all__ = ["add"]
```

**Build + editable install**
```bash
pip install -e .
python -c "from mypkg import add; print(add(2,3))"
```

**Sample `pyproject.toml` (setuptools)**
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypkg"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]
```

---

## 7) Quick “Osmosis” Exercises (5–10 min each)
- [ ] Create `mypkg` with `mathutils.add` + pytest.
- [ ] Add `black`, `isort`, `flake8` and run them.
- [ ] Add `mypy` and annotate `add` with types.
- [ ] Write a tiny Flask app with `/healthz` returning JSON and a failing test for `/missing` (404).

**Flask smoke (API)**  
```python
from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok"), 200

    return app

app = create_app()
```

**pytest for Flask route**
```python
from app import create_app

def test_healthz():
    client = create_app().test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}
```

---

## 8) Bitvocation CV‑Doctor: direct reusables
- **Package layout** under `src/` + editable install for shared lib (parsers, scorers, extractors).
- **Contracts**: define clear DTOs for CV input/output; validate with `pydantic` (optional).
- **Quality gates** in CI: `black`, `flake8`, `pytest`, and a minimal Playwright smoke for critical UI.
- **Observability**: standardized error JSON + route timings (later in Flask module).

---

## 9) Commands Cheat Sheet
```bash
# formatting & linting
black . && isort . && flake8 && pylint src

# tests
pytest -q

# editable install
pip install -e .

# quick Flask run (dev)
export FLASK_APP=app:app && flask run --debug
```

---

## 10) Snippet Library (copy/paste)
**`.gitignore` essentials**
```
__pycache__/
*.pyc
.venv/
.env
.dist/
build/
.coverage
.pytest_cache/
```

**`Makefile` (optional)**
```make
fmt:
	black .
	isort .

lint:
	flake8
	pylint src

test:
	pytest -q

all: fmt lint test
```

---

> Keep appending here as you progress. Next module: Flask deployment patterns (Gunicorn, containers, health endpoints, and minimal CI).

---

# Module 2 Living Notes — Flask Fundamentals & Deployment

## 0) TL;DR
- **Library vs Framework**: Libraries = pick-and-use tools; Frameworks = opinionated skeleton to plug your code into. Flask is a **microframework**—minimal core + extensions.
- **Flask basics**: app factory, routes, methods, dynamic URLs, request/response, status codes, error handlers, decorators.
- **CRUD**: build RESTful endpoints using GET/POST/PUT/PATCH/DELETE; handle forms with `request.form`.
- **Deploy**: don’t use Flask dev server in prod; use **Gunicorn** (or uWSGI) behind a reverse proxy; containerize for parity; provide `/healthz`.

## 1) Libraries vs Frameworks (in practice)
- **Library**: you call it. Examples: `requests`, `pandas`, `jinja2`.
- **Framework**: it calls **you** (inversion of control). Examples: **Flask**, **Django**, **FastAPI**.
- **Flask vs Django**
  - Flask: small core, flexible, choose-your-own DB/auth/ORM; great for focused services and APIs.
  - Django: batteries-included (ORM, admin, auth, templates) for large product stacks.

## 2) Flask Core: app, routes, methods, dynamic URLs
### App Factory (recommended)
```python
# src/app/__init__.py
from flask import Flask

def create_app(config_overrides: dict | None = None):
    app = Flask(__name__)
    app.config.update({"JSON_SORT_KEYS": False})
    if config_overrides:
        app.config.update(config_overrides)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    return app

# wsgi.py
from app import create_app
app = create_app()
```

### Routes + Methods
```python
from flask import request, jsonify

@app.route("/api/v1/items", methods=["GET", "POST"])
def items():
    if request.method == "GET":
        return jsonify(items=list_items()), 200
    data = request.get_json(silent=True) or {}
    created = create_item(data)
    return jsonify(created), 201
```

### Dynamic URLs + Converters
```python
@app.get("/api/v1/items/<int:item_id>")
def item_detail(item_id: int):
    item = get_item(item_id)
    if not item:
        return {"error": "not found"}, 404
    return item, 200
```

### url_for for robust links/redirects
```python
from flask import redirect, url_for

@app.get("/admin")
def admin():
    return redirect(url_for("login"))

@app.get("/login")
def login():
    return "<Login Page>"
```

## 3) Request & Response Objects
```python
from flask import request, make_response, jsonify

# Query params
q = request.args.get("q")             # /search?q=python
# Form data (POST form)
user = request.form.get("username")
# JSON body (application/json)
payload = request.get_json(silent=True) or {}
# Files
file = request.files.get("cv")

# Responses
return jsonify(result="ok"), 200
resp = make_response({"error": "nope"}, 422)
resp.headers["X-Trace"] = "abc123"
return resp
```

### HTTP Status Codes (common)
- 200 OK, 201 Created, 204 No Content  
- 400 Bad Request, **401 Unauthorized**, **403 Forbidden**, **404 Not Found**, 405 Method Not Allowed, 422 Unprocessable Entity  
- 429 Too Many Requests, 500 Internal Server Error

### Centralized Error Handling
```python
from flask import jsonify

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="resource not found"), 404

@app.errorhandler(500)
def internal(e):
    return jsonify(error="server error"), 500
```

## 4) Decorators in Flask
### Python function decorators (wrapping behavior)
```python
from functools import wraps

def jsonify_wrapper(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        return {"output": fn(*args, **kwargs)}
    return inner

@jsonify_wrapper
def hello():
    return "hello world"
```

### Route decorators (provided by Flask)
```python
@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return "Hello World!"
```

### Dynamic path segments
```python
@app.get("/userdetails/<userid>")
def user_details(userid: str):
    return f"User Details for {userid}"
```

## 5) CRUD Patterns (forms + JSON)
**Create (form POST → redirect)**
```python
from flask import request, redirect, url_for, render_template

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        record = create_new_record(name)
        return redirect(url_for("read", id=record.id))
    return render_template("create.html")
```

**Read**
```python
@app.get("/read/<int:id>")
def read(id: int):
    record = get_record(id)
    if not record:
        return {"error": "not found"}, 404
    return render_template("read.html", record=record)
```

**Update (GET form + POST submit)**
```python
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    if request.method == "POST":
        name = request.form["name"]
        update_record(id, name)
        return redirect(url_for("read", id=id))
    record = get_record(id)
    return render_template("update.html", record=record)
```

**Delete**
```python
@app.post("/delete/<int:id>")
def delete(id: int):
    delete_record(id)
    return redirect(url_for("home"))
```

> API-first variant: accept/return JSON with `Content-Type: application/json`, and use proper 201/204 codes.

## 6) Calling External APIs
```python
import requests

@app.get("/api/v1/search")
def search():
    term = request.args.get("q", "")
    try:
        r = requests.get("https://api.example.com/search", params={"q": term}, timeout=5)
        r.raise_for_status()
        return r.json(), 200
    except requests.RequestException as exc:
        return {"error": str(exc)}, 502
```

## 7) Deployment Basics (Prod)
- **Don’t** run the Flask dev server in production.
- Use **Gunicorn** (WSGI) and set `FLASK_ENV=production`.
- Keep secrets in env vars; separate config for dev/test/prod.
- Provide `/healthz` and structured logs.

**Gunicorn start**
```bash
gunicorn -w 2 -b 0.0.0.0:8000 "wsgi:app"
```

**Minimal Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel &&     pip install --no-cache-dir .
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
```

## 8) Bitvocation CV-Doctor — direct reusables (Module 2)
- **Blueprints**: split `api` vs `web` (upload form vs JSON endpoints).
- **Status discipline**: 201 for created CV, 422 for invalid file, 415 for wrong media type, 429 for rate limits.
- **Form + API parity**: support both `multipart/form-data` (web) and JSON (API).
- **External calls**: safely call LLM/scoring microservice with timeouts + retries; validate inputs first.
- **Security**: validate file type/size; consider CSRF for forms; consistent error JSON.

## 9) Cheat Sheet — Flask Web App & API
- Instantiate:
  ```python
  from flask import Flask
  app = Flask(__name__)
  ```
- Route:
  ```python
  @app.route("/")
  def hello_world():
      return "My first Flask app!"
  ```
- JSON + status:
  ```python
  from flask import jsonify
  return jsonify(message="ok"), 200
  ```
- Errors:
  ```python
  return {"error_message": "Input missing"}, 422
  ```
  ```python
  @app.errorhandler(500)
  def server_error(e):
      return {"message": "Something went wrong"}, 500
  ```
- Redirect + url_for:
  ```python
  return redirect(url_for("login"))
  ```
- Method handling:
  ```python
  @app.route("/data", methods=["GET","POST"])
  def data():
      if request.method == "POST":
          ...
      else:
          ...
  ```
- Dynamic route:
  ```python
  @app.get("/user/<int:id>")
  def get_user(id): ...
  ```

> Next up (Module 3): wire a small AI model, wrap with Flask, add tests & deploy. We’ll keep extending this doc with production patterns (auth, rate limiting, caching).

---

# Module 3 Living Notes — AI with Watson + Flask

## 0) TL;DR
- **Embeddable Watson AI** provides packaged NLP models (e.g., sentiment, emotion) preinstalled in the Skills Network Cloud IDE. Use them to add AI to Flask without training models.
- Build two apps:
  1) **Sentiment Analysis** (practice)  
  2) **Emotion Detection** (final, peer-reviewed)
- For both: package code, add unit tests, static analysis, and robust error handling; deploy via Flask/Gunicorn.

> If running locally (outside Skills Network), use a **provider adapter** pattern so you can swap in a fallback (e.g., Hugging Face) if Watson libs aren’t available.

## 1) Embeddable Watson AI: integration pattern
**Concept**
- Treat the AI inference as a function that returns a structured result (label, score, distribution).
- Wrap vendor specifics in an **adapter** so the rest of your app is provider-agnostic.

**Layout**
```
src/
  app/                # Flask app (routes, error handlers)
  ai_core/            # Provider-agnostic interfaces
    __init__.py
    types.py          # dataclasses / TypedDicts for outputs
    pipeline.py       # high-level sentiment/emotion functions
  ai_providers/
    watson_adapter.py # calls Embeddable Watson NLP
    hf_adapter.py     # fallback (e.g., transformers) if needed
tests/
```

**Interface example (`ai_core/types.py`)**
```python
from typing import TypedDict

class SentimentResult(TypedDict):
    label: str     # 'positive' | 'negative' | 'neutral'
    score: float   # 0..1

class EmotionResult(TypedDict):
    top: str                   # 'joy' | 'sadness' | ...
    scores: dict[str, float]   # label -> probability
```

**Provider selection (`ai_core/pipeline.py`)**
```python
import os
from ai_providers.watson_adapter import WatsonNLP
from ai_providers.hf_adapter import HFModels

PROVIDER = os.getenv("AI_PROVIDER", "watson")

def get_sentiment(text: str):
    if PROVIDER == "watson":
        return WatsonNLP.sentiment(text)
    return HFModels.sentiment(text)

def get_emotion(text: str):
    if PROVIDER == "watson":
        return WatsonNLP.emotion(text)
    return HFModels.emotion(text)
```

> Keep the **public contract** stable (same keys/status codes), regardless of provider.

## 2) Practice Project — Sentiment Analysis (Flask)
**API-first design**
- `POST /api/v1/sentiment` with JSON `{"text": "..."}`
- Response: `{"label": "positive", "score": 0.92}` (201 Created if you persist; 200 OK otherwise)
- Errors: `422` invalid input, `413` too large, `502` up/downstream failure

**Routes (`app/routes_sentiment.py`)**
```python
from flask import Blueprint, request, jsonify
from ai_core.pipeline import get_sentiment

bp = Blueprint("sentiment", __name__)

@bp.post("/api/v1/sentiment")
def sentiment():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return {"error": "text is required"}, 422
    if len(text) > 10_000:
        return {"error": "text too long"}, 413
    try:
        res = get_sentiment(text)
        return jsonify(res), 200
    except Exception as exc:
        return {"error": str(exc)}, 502
```

**Unit tests (pytest)**
```python
def test_sentiment_happy(client):
    r = client.post("/api/v1/sentiment", json={"text": "I love Python and Flask"})
    assert r.status_code == 200
    body = r.get_json()
    assert "label" in body and "score" in body

def test_sentiment_empty(client):
    r = client.post("/api/v1/sentiment", json={"text": ""})
    assert r.status_code == 422
```

> Add a `client` fixture that uses `create_app(testing=True).test_client()`.

**UI (optional)**
- Simple form + result card; show label/score.
- Keep the same API so Playwright smoke tests can exercise both UI and API.

## 3) Final Project — Emotion Detection (Flask)
**API-first**
- `POST /api/v1/emotion` with `{"text": "..."}`
- Response:
```json
{
  "top": "joy",
  "scores": {"joy": 0.78, "sadness": 0.05, "anger": 0.04, "fear": 0.03, "disgust": 0.10}
}
```

**Routes (`app/routes_emotion.py`)**
```python
from flask import Blueprint, request, jsonify
from ai_core.pipeline import get_emotion

bp = Blueprint("emotion", __name__)

@bp.post("/api/v1/emotion")
def emotion():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return {"error": "text is required"}, 422
    try:
        res = get_emotion(text)
        # Optional: normalize to sum=1.0
        total = sum(res["scores"].values()) or 1.0
        res["scores"] = {k: v/total for k, v in res["scores"].items()}
        return jsonify(res), 200
    except Exception as exc:
        return {"error": str(exc)}, 502
```

**UI**
- Bar chart of probabilities (Chart.js) + highlighted top emotion.
- Friendly error messages; keep the page responsive for mobile.

## 4) Packaging for deployment
- `pyproject.toml` with `project.scripts` entry point; `src/` layout; `wsgi.py` for Gunicorn.
- Config via env vars: `AI_PROVIDER`, `MAX_TEXT_LEN`, `LOG_LEVEL`.
- Keep **adapters** in separate module so you can publish the non-proprietary parts publicly.

**Example `pyproject.toml` excerpt**
```toml
[project]
name = "ai-flask-apps"
version = "0.1.0"
dependencies = [
  "flask>=3.0",
  "requests>=2.32",
  # "watson-nlp-embed"  # placeholder: provided in Skills Network
]

[tool.setuptools.packages.find]
where = ["src"]
```

## 5) Static code analysis & QA gates (reuse from Modules 1–2)
- Format: `black`, imports: `isort`, style: `flake8`, lint: `pylint`, types: `mypy` (optional).
- Security: add `bandit` for Python security checks.
- CI job: run linters + tests on push/PR; fail fast on violations.

**Bandit**
```bash
pip install bandit
bandit -r src
```

## 6) Error handling patterns
- Validate input early; return `422` with clear messages.
- Catch adapter exceptions and return `502` (bad gateway) if the AI provider fails.
- Log with request IDs (e.g., `X-Request-Id`) to trace issues end-to-end.

**Centralized handlers (`app/errors.py`)**
```python
from flask import Blueprint, jsonify

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def not_found(e):
    return jsonify(error="resource not found"), 404

@errors.app_errorhandler(500)
def server_error(e):
    return jsonify(error="internal server error"), 500
```

## 7) Deployment (prod)
- Gunicorn behind reverse proxy (Render/Fly/railway/Heroku-like); `/healthz` for probes.
- Minimal resources: 2 workers; set timeouts and request body limits.
- Keep secrets (API keys if any) out of the repo; use environment variables.

**Gunicorn**
```bash
gunicorn -w 2 -b 0.0.0.0:8000 "wsgi:app"
```

**Health check**
```python
@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200
```

## 8) Peer-review checklist (rubric-ready)
- [ ] Clean, PEP8-compliant code; passes `black`/`flake8`.
- [ ] Clear packaging (`src/` layout, `pyproject.toml`).
- [ ] Unit tests for functions and routes (happy/edge/error paths).
- [ ] Sensible HTTP statuses and JSON error format.
- [ ] Input validation + length limits.
- [ ] Provider-agnostic adapters; graceful fallback or error.
- [ ] README with run steps, screenshots, and API examples.
- [ ] Deployed demo URL (optional but strong).

## 9) Bitvocation CV-Doctor tie-ins (reusables)
- Reuse the **adapter pattern** for model providers (Watson vs OpenAI/HF) for CV parsing/scoring.
- Standardize JSON contracts for score outputs so UI & tests stay stable.
- Add Playwright smoke: upload → parse → score → result visible.
- Log + metrics around input size and processing time for triage.

---

## Quizzes & Answers (to append as you complete)
> Paste the quiz question in shorthand, then your answer & reasoning.

### Module 1 Quiz Notes
- Q: …  
  A: … (Why: …)
- Q: …  
  A: …

### Module 2 Quiz Notes
- Q: …  
  A: … (Why: …)
- Q: …  
  A: …

### Module 3 Quiz Notes
- Q: …  
  A: … (Why: …)
- Q: …  
  A: …

---

## Module 1 — Graded Quiz Answers (with brief reasoning)

1) **An API that connects the browser and the application.**  
   *Reason:* The browser talks to the backend via HTTP endpoints (the API).

2) **Integration testing**  
   *Reason:* You’re validating a new payment gateway works with the existing system components.

3) **PyLint is a Python static code analysis tool.**  
   *Reason:* It analyzes code quality/style without executing it.

4) **DATE_OF_BIRTH**  
   *Reason:* PEP8 constants use UPPER_SNAKE_CASE.

5) **User requirements**  
   *Reason:* “Enable users to view rooms/amenities” describes user‑visible functionality.

6) **It organizes assertion logic separately.**  
   *Reason:* `unittest.TestCase` groups related tests, enabling setup/teardown and clear structure.

7) **The doubler function displayed the wrong result, hence the assertion failed.**  
   *Reason:* Expected 6, got 9 → implementation isn’t meeting the spec.

8) **from mypackage import my_code;  my_code.print_hello()**  
   *Reason:* Import the module from the package, then call the function on that module.

9) **{package_name}.{module_name}.{function_name}(parameters)**  
   *Reason:* Standard dotted import call pattern for package → module → function.

10) **A library recognized as a Python package.**  
    *Reason:* A folder with `__init__.py` and .py modules is a Python package.

---

## Module 2 — Graded Quiz Answers (with brief reasoning)

1) **Frameworks provides reusable modules, structured flow, and support for full application development.**  
   *Reason:* Frameworks (Flask/Django) give an app skeleton and patterns; libraries are piecemeal tools.

2) **Route**  
   *Reason:* The URL is mapped to a *route* whose view function runs and returns the response.

3) **URL handlers**  
   *Reason:* `@app.route()` decorates a function to *handle* a specific URL pattern.

4) **content_length**  
   *Reason:* This property reports the response body size (bytes). `content_type` is MIME; `status_code` is HTTP code.

5) **request.access_route**  
   *Reason:* Returns the list of proxy IPs + client address in order.

6) **Deliver the response's JSON data in the frontend.**  
   *Reason:* 200 OK means success—use/parse the JSON in your UI.

7) **Three**  
   *Reason:* HTTP status codes are 3 digits (e.g., 200, 404, 500).

8) **200**  
   *Reason:* Flask returns 200 OK by default if the route returns successfully.

9) **The route will accept the GET request automatically.**  
   *Reason:* Without `methods=[...]`, Flask allows GET (plus HEAD/OPTIONS automatically).

10) **Use PUT or PATCH requests to change the existing database.**  
    *Reason:* Conventional REST: PUT/PATCH for update, POST for create, DELETE for delete, GET for read.

---

# Final Project — Emotion Detection (Working Notes)

## 0) One-liner
Build a Flask web/API app that detects **emotion** from input text using **Embeddable Watson AI** (adapter pattern ready for alternate providers). Ship with unit tests, static analysis, and robust error handling.

## 1) Requirements (draft)
- Input: plain text (UTF-8), JSON body `{ "text": "..." }`.
- Output (JSON): `{ "top": "<emotion>", "scores": { "<emotion>": <0..1>, ... } }`.
- Constraints: max length, allowed content types, timeouts.
- Non-functionals: latency target, health endpoint, logging, containerized deploy.

## 2) API Contract
- `POST /api/v1/emotion`
  - Request: JSON `{ "text": "..." }`
  - Responses:
    - `200 OK` – result payload
    - `422 Unprocessable Entity` – validation error
    - `502 Bad Gateway` – provider failure
- `GET /healthz` → `{ "status": "ok" }`

## 3) Data Flow
Client → Flask route → `ai_core.pipeline.get_emotion(text)` → provider adapter (Watson) → normalize → JSON response.

## 4) Test Plan (pytest)
- Happy paths: common phrases return a top emotion + normalized scores (sum≈1.0).
- Edge cases: empty text (422), too long (413), unsupported content type (415).
- Error: simulate provider exception → 502.
- Contract tests: keys present, types correct, probabilities within [0,1].

## 5) Static Analysis & Quality Gates
- `black`, `isort`, `flake8`, `pylint`, optional `mypy`.
- `bandit -r src` for security checks.

## 6) Error Handling
- Centralized Blueprint for 404/500.
- Clear JSON messages; no stack traces in prod.
- Input validation before provider call.

## 7) Packaging & Deploy
- `src/` layout + `pyproject.toml`.
- `wsgi.py` for Gunicorn; Dockerfile for prod parity.
- ENV: `AI_PROVIDER`, `MAX_TEXT_LEN`, `LOG_LEVEL`.

## 8) UI (optional)
- Minimal page: textarea → submit → result cards/bar chart.
- Show top emotion prominently.

## 9) Peer-Review Checklist
- [ ] Clean code & style pass
- [ ] Tests (routes + core)
- [ ] Sensible statuses & messages
- [ ] Docs: README with run steps + screenshots
- [ ] Deployed demo (optional)

> Paste raw notes from the project below; we’ll refine into the sections above.

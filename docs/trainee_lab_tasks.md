git# 🧪 GitHub Copilot Training — Lab Tasks
### Conduit · FastAPI RealWorld · 10-Day Programme

> **Before you start each day**
> - Check out your personal branch: `git checkout -b feature/<your-name>`
> - All work goes into this branch — never commit directly to `main`
> - Use `notes/` folder for daily reflections and observations

---

## Repository Layout

```
conduit-copilot-training/
├── app/                          # FastAPI Conduit source
├── tests/
│   ├── unit/                     # Day 2
│   ├── e2e/                      # Day 3
│   │   └── pages/                # Page Object Model classes
│   └── api/                      # Day 4
├── .github/
│   ├── workflows/                # Day 5
│   └── copilot-instructions.md   # Day 1 setup
├── infra/
│   ├── k8s/                      # Day 6 (core)
│   └── terraform/                # Day 6 (stretch)
├── monitoring/                   # Day 7
├── scripts/                      # Days 5, 7, 8
└── notes/                        # Your daily reflections
```

---


## Day 1 — Copilot Orientation

**Goal:** Make your first successful Copilot suggestion in the Conduit codebase and understand how context shapes suggestion quality.

**Setup checklist:**
- [ ] Copilot extension installed and authenticated in VS Code
- [ ] Repo cloned, `pip install -r requirements.txt` done
- [ ] Database running: `docker-compose up -d db`

---

### Core Tasks

#### 1.1 — Explore with Copilot Chat
Open `app/api/routes/articles.py`. Use Copilot Chat and ask:
- *"Explain what this file does and list all endpoints"*
- *"What database models does this router depend on?"*

Save your findings to `notes/day1_exploration.md`.

#### 1.2 — Comment-driven completion
Open `app/services/articles.py`. Above an empty function stub, write a docstring comment describing:
- **Input:** `title: str`, `body: str`, `author_id: int`
- **Output:** `slug` — URL-safe, unique string
- **Edge case:** duplicate slug must append a short random suffix

Accept Copilot's completion. Then remove the edge-case line and regenerate — observe how the suggestion changes.

#### 1.3 — Refine with inline chat
Select the code from 1.2. Use inline chat (`Ctrl+I`) to:
- *"Make this async"*
- *"Add type hints to all parameters"*
- *"Extract the slug suffix logic into a separate testable helper function"*

Commit the refined function to your branch.

#### 1.4 — Generate documentation
From the repo root in Copilot Chat, prompt:
> *"Generate a Getting Started section for this FastAPI RealWorld app — include local setup, required environment variables, and how to run the tests"*

Save output to `notes/day1_readme_draft.md`.

---

### Optional Tasks *(if time allows)*

#### 1.5 — Dependency mapping
Ask Copilot Chat: *"Draw an ASCII diagram showing how the articles router, article service, and User/Article models relate to each other."* Add to `notes/day1_exploration.md`.

#### 1.6 — Context window experiment
Ask the same question as 1.1 — once with only the route file open, and once with the model and service files also open. Note any difference in answer quality.

---

### Reflection
> Save to `notes/day1_reflection.md`
1. What made suggestions better or worse today?
2. Which part of the codebase was easiest / hardest to prompt about?

---

## Day 2 — Unit Test Generation

**Goal:** Generate a working unit test suite for Conduit's service layer — no database, no HTTP calls.

**Setup checklist:**
- [ ] Day 1 complete and committed
- [ ] `pytest`, `pytest-asyncio`, `pytest-mock` installed
- [ ] `tests/unit/` folder exists and empty

---

### Core Tasks

#### 2.1 — Slug utility tests
Open the slug helper from Day 1. In Copilot Chat, use the `/tests` command:
```
/tests Generate unit tests covering:
- happy path (normal title)
- empty title input
- title with special characters and spaces
- duplicate slug collision handling
```
Save to `tests/unit/test_slug_utils.py`. Run: `pytest tests/unit/ -v`

#### 2.2 — Auth service tests
Open `app/services/auth.py`. Write this comment above `verify_password`:
```python
# Unit tests needed:
# - correct password returns True
# - wrong password returns False
# - empty string returns False
# - bcrypt error is handled gracefully
```
Accept completions. Save to `tests/unit/test_auth_service.py`.

#### 2.3 — Mock database calls
Open `app/services/articles.py` → `get_article_by_slug()`. Prompt:
> *"Write unit tests for `get_article_by_slug` that mock the `AsyncSession`. Cover: article found, article not found returns None, DB raises an exception."*

Save to `tests/unit/test_article_service.py`.

#### 2.4 — Fix failing tests
Run `pytest tests/unit/ -v`. For any failure, use inline chat:
> *"Fix this test — the mock is not being applied correctly"*

Document what Copilot got wrong on the first attempt in `notes/day2_fixes.md`.

---

### Optional Tasks

#### 2.5 — Coverage report *(stretch)*
```bash
pytest tests/unit/ --cov=app/services --cov-report=term-missing
```
Find any uncovered branch and ask Copilot to generate a test for it.

#### 2.6 — Parametrize a test *(stretch)*
Ask Copilot to rewrite one of your test functions using `@pytest.mark.parametrize` to cover 5 input variations in a single test.

---

### Acceptance Criteria
- [ ] Minimum **10 test functions** across all files
- [ ] No real DB or HTTP calls in any test
- [ ] `pytest tests/unit/` exits with zero failures

---

## Day 3 — Playwright E2E Automation

**Goal:** Build a Playwright test suite for Conduit's core user journeys using the Page Object Model.

**Setup checklist:**
- [ ] App running: `uvicorn app.main:app --reload`
- [ ] Frontend running at `http://localhost:3000`
- [ ] `playwright install chromium` done

---

### Core Tasks

#### 3.1 — LoginPage object
Create `tests/e2e/pages/login_page.py`. Write this comment and let Copilot complete:
```python
# Page Object for the Conduit login page at /login
# Locators: email input (by label), password input (by label), submit button (by role)
# Methods: navigate(), login(email, password), get_error_message()
# All methods must be async
```
Validate generated locators against the actual running UI.

#### 3.2 — ArticleEditorPage object
Create `tests/e2e/pages/article_editor_page.py`. Prompt:
> *"Generate a POM class for the Conduit article editor at /editor. Methods: navigate(), fill_title(), fill_description(), fill_body(), add_tag(), publish() → returns the published article slug from the URL"*

#### 3.3 — Test scenarios
Create `tests/e2e/test_article_lifecycle.py`. Write these stubs — let Copilot fill them:
```python
# Test 1: Registered user can log in and see their feed
# Test 2: Logged-in user can create an article and it appears on their profile
# Test 3: Login with invalid credentials shows an error message
# Test 4: Unauthenticated user is redirected when accessing /editor
```

#### 3.4 — Authenticated session fixture
In `tests/e2e/conftest.py`, prompt:
> *"Write a pytest fixture that logs in with test credentials, saves browser storage state to a file, and provides an authenticated page to all tests — so login only happens once per test run"*

---

### Optional Tasks

#### 3.5 — Comment flow test *(stretch)*
Add a fifth test:
> *"Logged-in user can add a comment to an article and it appears in the comments list"*

#### 3.6 — Cross-browser *(stretch)*
Ask Copilot to add `@pytest.mark.parametrize` to run all tests on both Chromium and Firefox.

---

### Acceptance Criteria
- [ ] All POM classes use `get_by_role()` / `get_by_label()` — **no raw CSS selectors**
- [ ] **No `waitForTimeout()`** anywhere in test files
- [ ] `pytest tests/e2e/ --headed` completes without manual intervention

---

## Day 4 — API Test Suite

**Goal:** Build a complete API test suite for Conduit endpoints using `pytest` + `httpx.AsyncClient`.

**Setup checklist:**
- [ ] App running, Swagger visible at `http://localhost:8000/docs`
- [ ] `httpx`, `pytest-asyncio` installed
- [ ] `tests/api/conftest.py` scaffold (provided by trainer) with `async_client` and `auth_headers` fixtures

---

### Core Tasks

#### 4.1 — Auth endpoint tests
Create `tests/api/test_auth.py`. Open `POST /api/users/login` in Swagger. Prompt:
> *"Generate pytest async tests for POST /api/users/login. Cover: valid credentials return 200 with token, wrong password returns 422, non-existent user returns 422, missing email field returns 422"*

#### 4.2 — Articles CRUD tests
Create `tests/api/test_articles.py`. Write these stubs:
```python
# Test: Create article — authenticated, valid payload → 201 with slug
# Test: Create article — unauthenticated → 401
# Test: Get article by slug → 200 with correct title
# Test: Update article — change title → 200, slug regenerated
# Test: Delete article — author → 204
# Test: Delete article — non-author → 403
```

> ⚠️ **Watch out:** Copilot often generates `Authorization: Bearer <token>`.  
> The Conduit API requires `Authorization: Token <jwt>` — fix any instance of this.

#### 4.3 — Pagination and filtering
Create `tests/api/test_articles_list.py`. Prompt:
> *"Generate tests for GET /api/articles that verify: default limit is 20, limit and offset params work, filtering by tag returns only tagged articles, filtering by author returns only that author's articles"*

#### 4.4 — Boundary tests
In `tests/api/test_articles.py`, prompt:
> *"Add boundary tests: article body at 0 characters, title at 256 characters — assert the correct status codes"*

---

### Optional Tasks

#### 4.5 — Postman collection *(stretch)*
> *"Based on the tests in `tests/api/`, generate a Postman collection JSON with a pre-request script that sets the auth token from an environment variable"*

Save to `tests/api/conduit.postman_collection.json`.

#### 4.6 — Tags and profiles *(stretch)*
Add tests for `GET /api/tags` and `GET /api/profiles/:username` in `tests/api/test_profiles_tags.py`.

---

### Acceptance Criteria
- [ ] Minimum **20 test functions** across all API test files
- [ ] Status code is **always the first assertion** in every test
- [ ] `Authorization: Token` prefix used throughout — not `Bearer`
- [ ] `pytest tests/api/ -v` exits 0

---

## Day 5 — CI/CD with GitHub Actions

**Goal:** Build a complete GitHub Actions pipeline — lint, unit tests, API tests, Docker build.

**Setup checklist:**
- [ ] Days 1–4 complete and tests passing locally
- [ ] Docker installed
- [ ] GitHub repo exists with Actions enabled

---

### Core Tasks

#### 5.1 — Generate the CI workflow
Create `.github/workflows/ci.yml`. Write this comment block:
```yaml
# CI workflow — triggered on push and pull_request to any branch
# Jobs:
#   lint: black --check, isort --check, ruff on app/ and tests/
#   unit-tests: pytest tests/unit/ with coverage
#   api-tests: postgres service container + pytest tests/api/
# All jobs: ubuntu-latest, Python 3.11, actions/cache for pip
```
Let Copilot complete the full YAML.

#### 5.2 — Docker build job
After the `api-tests` job, prompt:
> *"Add a `docker-build` job that depends on `api-tests`, builds the Dockerfile tagged with the git SHA, and pushes to GitHub Container Registry using GITHUB_TOKEN"*

#### 5.3 — Health-check script
Create `scripts/health_check.py`. Write this comment:
```python
# Deployment health check script
# Checks: /health → 200, /api/tags → 200 with valid JSON, response < 2 seconds
# Retries up to 5 times with 10-second backoff
# Exits code 1 on any failure — designed for use as a CI step
# BASE_URL from first CLI argument or APP_URL environment variable
```

#### 5.4 — Status badge and summary job
Prompt:
> *"Add a `report` job that runs after all other jobs and exits 1 if any upstream job failed. Also generate the workflow status badge markdown for the README."*

---

### Optional Tasks

#### 5.5 — E2E workflow *(stretch)*
Create `.github/workflows/e2e.yml`:
> *"GitHub Actions workflow that runs Playwright tests only on push to main. Starts the full stack with docker-compose, waits for health check, runs pytest tests/e2e/, uploads HTML report as artifact on failure"*

#### 5.6 — Dependabot config *(stretch)*
Ask Copilot to generate `.github/dependabot.yml` for weekly pip updates and monthly Actions version updates.

---

### Acceptance Criteria
- [ ] No hardcoded secrets — all use `${{ secrets.* }}`
- [ ] Docker image tagged with `${{ github.sha }}` — **never `latest`**
- [ ] `actions/cache` used for pip in all jobs

---

## Day 6 — Infrastructure as Code

**Goal:** Generate production-grade Kubernetes manifests for Conduit using Copilot. Terraform is a stretch goal.

**Setup checklist:**
- [ ] Docker image from Day 5 pushed to GHCR
- [ ] `kubectl` installed
- [ ] `infra/k8s/` and `infra/terraform/` folders exist and empty

---

### Core Tasks

#### 6.1 — Deployment manifest
Create `infra/k8s/deployment.yaml`. Write this comment:
```yaml
# Kubernetes Deployment for Conduit FastAPI
# Image: ghcr.io/<org>/conduit:<git-sha>
# Replicas: 2, container port: 8000
# Resources: requests cpu=100m mem=128Mi / limits cpu=500m mem=512Mi
# Liveness probe: GET /health, initialDelaySeconds 30
# Readiness probe: GET /health, initialDelaySeconds 10
# Env vars from ConfigMap and Secret
```

#### 6.2 — Service and Ingress
Create `infra/k8s/service.yaml` and `infra/k8s/ingress.yaml`. Prompt:
> *"Generate a ClusterIP Service on port 80 targeting container port 8000, and an Nginx Ingress with TLS termination and host `conduit.training.internal`"*

#### 6.3 — ConfigMap and Secret
Create `infra/k8s/configmap.yaml` and `infra/k8s/secret.yaml`. Prompt:
> *"Generate a ConfigMap for non-sensitive config (DB host, allowed origins) and a Secret template for DB password and JWT secret key — use base64 placeholder comments for secret values"*

#### 6.4 — Validate
```bash
kubectl apply --dry-run=client -f infra/k8s/
```
For each validation error, paste it into Copilot inline chat:
> *"Fix this Kubernetes validation error: [paste error]"*

---

### Optional Tasks

#### 6.5 — Terraform EKS node group *(stretch)*
Create `infra/terraform/main.tf`. Prompt:
> *"Terraform config for an EKS managed node group: VPC data source, t3.medium instances, min 1 max 3 nodes, required IAM role, outputs for cluster endpoint"*

Run `terraform init && terraform validate`.

#### 6.6 — Multi-stage Dockerfile *(stretch)*
> *"Rewrite the existing Dockerfile as a multi-stage build where the final image runs as a non-root user with no dev dependencies"*

---

### Acceptance Criteria
- [ ] `kubectl apply --dry-run=client -f infra/k8s/` exits 0
- [ ] All containers have `resources.requests` and `resources.limits`
- [ ] Image tag is parameterised — no hardcoded SHA

---

## Day 7 — Monitoring, Logging & SRE

**Goal:** Instrument Conduit with Prometheus metrics, write alerting rules, and build a log parser.

**Setup checklist:**
- [ ] `prometheus-fastapi-instrumentator` installed
- [ ] Prometheus running via `docker-compose`
- [ ] `monitoring/` folder exists

---

### Core Tasks

#### 7.1 — Add Prometheus instrumentation
Open `app/main.py`. Prompt:
> *"Add prometheus-fastapi-instrumentator to this FastAPI app, expose metrics at /metrics, and add a custom counter `conduit_articles_created_total` that increments on each successful POST /api/articles"*

Verify: `curl http://localhost:8000/metrics`

#### 7.2 — Alerting rules
Create `monitoring/alert_rules.yml`. Write these stubs:
```yaml
# Alert 1: ConduitHighErrorRate — 5xx rate > 5% over 5 minutes
# Alert 2: ConduitHighLatency — p99 > 500ms over 10 minutes
# Alert 3: ConduitDBConnectionsExhausted — pool > 80% full
# Alert 4: ConduitPodRestarting — restarts > 3 in 15 minutes
# All alerts: severity label + runbook_url annotation
```
Validate: `promtool check rules monitoring/alert_rules.yml`

#### 7.3 — Log parser script
Create `scripts/log_parser.py`. Write this comment:
```python
# Parse Conduit structured JSON access logs and report:
# - Top 10 slowest endpoints (avg response time)
# - Top 5 most frequent error paths (4xx + 5xx)
# - Requests per minute for the last hour
# - trace_ids appearing > 20 times (loop detection)
# Input: log file path as CLI argument
# Output: formatted summary table to stdout
# Must handle malformed/non-JSON lines without crashing
```

#### 7.4 — SLO PromQL queries
Create `monitoring/slo_queries.md`. Prompt:
> *"Generate PromQL queries for: 99.5% availability SLO over 30 days, p99 write endpoint latency under 500ms, error budget burn rate alert for 5% monthly budget in 1 hour"*

---

### Optional Tasks

#### 7.5 — Synthetic monitor *(stretch)*
Create `scripts/synthetic_monitor.py`:
> *"Python script that runs a synthetic transaction every 60 seconds: register user → create article → fetch article → delete it. Record per-step latency to `metrics.csv`. Exit cleanly on SIGINT."*

#### 7.6 — Grafana dashboard *(stretch)*
> *"Generate a Grafana dashboard JSON with three panels: request rate, p99 latency, and error rate for the Conduit app using Prometheus data source"*

Save to `monitoring/grafana_dashboard.json`.

---

### Acceptance Criteria
- [ ] `GET /metrics` returns `conduit_`-prefixed custom metric
- [ ] `promtool check rules monitoring/alert_rules.yml` passes with 0 errors
- [ ] Log parser runs on sample log without crashing

---

## Day 8 — Debugging & Secure Coding

**Goal:** Use Copilot `/fix`, code review, and security-aware suggestions to find and fix intentional bugs in the `day8-bugs` branch.

**Setup checklist:**
- [ ] `pip install bandit`
- [ ] Check out the bugs branch: `git fetch && git checkout day8-bugs`

> ℹ️ This branch has **6 intentional bugs** injected by your trainer. Your job is to find and fix them using Copilot.

---

### Core Tasks

#### 8.1 — Fix the SQL injection
Find the raw f-string SQL query in `app/services/articles.py` → `get_articles_by_tag()`. Use inline chat:
> *"This query is vulnerable to SQL injection. Rewrite it using SQLAlchemy parameterised bindings"*

Write a regression test in `tests/unit/test_security.py` that passes a malicious tag value `'; DROP TABLE articles; --` and confirms no error.

#### 8.2 — Fix the hardcoded secret
Find the hardcoded JWT secret in `app/core/config.py`. Prompt:
> *"Replace this hardcoded secret with a Pydantic Settings field reading from the SECRET_KEY environment variable that raises a clear startup error if not set"*

#### 8.3 — Fix the JWT expiry bypass
The `get_current_user` dependency allows expired tokens through. Paste the function into Copilot Chat:
> *"This JWT verification is not checking expiry. Identify the bug, fix it, and add a unit test confirming an expired token raises HTTPException 401"*

#### 8.4 — Run Bandit
```bash
bandit -r app/ -ll -f json -o notes/day8_bandit.json
```
For each HIGH or MEDIUM finding, prompt:
> *"Bandit reports: [paste finding]. Fix this security issue."*

Document each fix in `notes/day8_security_fixes.md`.

---

### Optional Tasks

#### 8.5 — Copilot Code Review *(stretch)*
Open a PR from your branch to `main`. Enable Copilot Code Review. Accept at least 2 suggestions. Reject at least 1 — write your justification in `notes/day8_review_decisions.md`.

#### 8.6 — Fix the N+1 query *(stretch)*
Find the N+1 query in `list_articles_with_author()`. Prompt:
> *"This produces N+1 database queries. Rewrite using SQLAlchemy eager loading with selectinload"*

---

### Acceptance Criteria
- [ ] `bandit -r app/ -ll` — **zero HIGH severity findings**
- [ ] All three core bugs fixed (SQL injection, hardcoded secret, JWT expiry)
- [ ] Each fix has a regression test in `tests/unit/test_security.py`

---

## Day 9 — Advanced Prompt Engineering

**Goal:** Master few-shot prompting, chained prompts, and workspace-level instructions to build a reusable team Copilot workflow.

**Setup checklist:**
- [ ] Days 1–8 complete and codebase in clean state
- [ ] `.github/copilot-instructions.md` from Day 1 setup

---

### Core Tasks

#### 9.1 — Few-shot test generation
Open `tests/api/test_comments.py` (empty). Manually write 3 example test functions at the top matching your team's agreed pattern, then add:
```python
# Following the exact pattern above, generate tests for:
# - POST /api/articles/:slug/comments (authenticated, unauthenticated, article not found)
# - GET /api/articles/:slug/comments (returns list, empty list)
# - DELETE /api/articles/:slug/comments/:id (author can delete, non-author cannot)
```
Compare quality vs. a zero-shot attempt. Note differences in `notes/day9_fewshot_comparison.md`.

#### 9.2 — Update copilot-instructions.md
Add a new section to `.github/copilot-instructions.md` based on your experience from Days 1–8:
- 2–3 new "What Copilot Should NOT Generate" rules you discovered
- One concrete few-shot example for your team's test pattern

Document changes in `notes/day9_instructions_changes.md`.

#### 9.3 — Build the Bookmark feature
Use a **chained prompt sequence** to build a new feature end-to-end — a user can bookmark an article and retrieve their bookmarks list:

1. *"Design the SQLAlchemy async model for a Bookmark with `user_id`, `article_id`, unique constraint, and cascade delete"*
2. *"Generate Pydantic v2 schemas for bookmark creation response and bookmark list response"*
3. *"Generate a FastAPI router with POST /api/articles/:slug/bookmark and GET /api/user/bookmarks"*
4. *"Generate unit tests for the bookmark service mocking AsyncSession"*
5. *"Generate API tests for the bookmark endpoints using the existing auth_headers fixture"*

#### 9.4 — Prompt library
Create `notes/day9_prompt_library.md` documenting your **10 most effective prompts** from the entire training:

| # | Prompt | Best used in | Rating (1–5) | How to improve it |
|---|--------|-------------|--------------|-------------------|
| 1 | ...    | ...         | ...          | ...               |

---

### Optional Tasks

#### 9.5 — Context window experiment *(stretch)*
Ask the same question about `app/api/routes/articles.py` twice — once with only that file open, once with model + schema + service files also open. Document in `notes/day9_context_experiment.md`.

---

### Acceptance Criteria
- [ ] `pytest tests/api/test_comments.py` — all generated tests pass
- [ ] Bookmark feature: model + router + at least **4 passing tests**
- [ ] `notes/day9_prompt_library.md` has 10 documented prompts

---

## Day 10 — Capstone Project

**Goal:** Deliver a complete, integrated quality engineering and DevOps setup for Conduit — every folder populated, every pipeline green.

---

### Definition of Done

| Area | Location | Requirement |
|------|----------|-------------|
| Unit Tests | `tests/unit/` | ≥ 15 test functions across ≥ 3 service modules |
| API Tests | `tests/api/` | ≥ 20 test functions covering auth, articles, comments |
| E2E Tests | `tests/e2e/` | ≥ 4 Playwright scenarios using POM pattern |
| CI Pipeline | `.github/workflows/ci.yml` | Lint + unit + API jobs defined and green |
| Docker Build | CI `docker-build` job | Image tagged with git SHA |
| K8s Manifests | `infra/k8s/` | deployment + service + configmap + secret present |
| Alert Rules | `monitoring/alert_rules.yml` | ≥ 4 rules, `promtool check` passes |
| Log Parser | `scripts/log_parser.py` | Runs on sample log without error |
| Health Check | `scripts/health_check.py` | Exits 0 on live app, exits 1 on bad URL |
| Copilot Config | `.github/copilot-instructions.md` | Updated with your team rules from Day 9 |

---

### Tasks

#### 10.1 — Gap audit *(30 min)*
```bash
pytest tests/ -v --tb=short
```
List every failing test and missing required file. Use Copilot to close gaps — prioritise API tests, then unit tests, then E2E.

#### 10.2 — Integration wire-up *(40 min)*
- Ensure CI runs: unit → API → docker-build → health check as final step
- All secrets use `${{ secrets.* }}`
- Push to your branch and confirm the Actions run completes green

#### 10.3 — Monitoring validation *(20 min)*
- `GET /metrics` returns `conduit_`-prefixed custom metric
- `promtool check rules monitoring/alert_rules.yml` passes
- `python scripts/log_parser.py sample_logs/conduit.log` runs without error

#### 10.4 — Presentation *(30 min — 5 min per participant)*
Demo these five items live:
1. `pytest tests/ --tb=short` — show current state
2. One Playwright test running headed: `pytest tests/e2e/ -k "test_login" --headed`
3. GitHub Actions — show latest CI run
4. `GET /metrics` in browser showing `conduit_articles_created_total`
5. Read one prompt from `notes/day9_prompt_library.md` — your most valuable

#### 10.5 — Retrospective *(submit before leaving)*
Create `notes/capstone_retro.md`:
```markdown
## 3 things Copilot did well
1.
2.
3.

## 3 things that needed manual correction
1.
2.
3.

## 1 rule I would add to copilot-instructions.md for my real project
```

---

*Document v1.0 — April 2026 | GitHub Copilot Training, Cohort 1*

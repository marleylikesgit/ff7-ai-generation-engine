# Deploying to Render (all-in-one)

This app has three pieces, all hosted on Render:

| Piece    | Render service type | Source dir |
|----------|---------------------|------------|
| Postgres | Managed Postgres (pgvector) | — |
| Backend  | Web Service (Python / FastAPI) | `backend/` |
| Frontend | Static Site (React / CRA) | `frontend/` |

A [`render.yaml`](./render.yaml) blueprint defines all three. You can deploy via
the blueprint (recommended) or create each service by hand.

---

## 1. Deploy the blueprint

1. Push this repo to GitHub.
2. In Render: **New → Blueprint**, pick this repo. Render reads `render.yaml`
   and proposes the Postgres DB + two web services.
3. Apply. The database and backend `DATABASE_URL` are wired automatically.

## 2. Set the secrets / URL env vars

Some values can't be baked into the blueprint and must be set in the dashboard:

**Backend service (`ff7-backend`):**

| Env var | Value |
|---------|-------|
| `OPENAI_API_KEY` | your OpenAI key (`sk-...`) |
| `FRONTEND_ORIGIN` | the frontend URL once it's live, e.g. `https://ff7-frontend.onrender.com` (no trailing slash) |

**Frontend service (`ff7-frontend`):**

| Env var | Value |
|---------|-------|
| `REACT_APP_API_BASE_URL` | the backend URL, e.g. `https://ff7-backend.onrender.com` (no trailing slash) |

> There's an unavoidable chicken-and-egg here: each service needs the other's
> URL. Deploy first, copy the two `onrender.com` URLs from the dashboard, paste
> them into the env vars above, then **redeploy both** (the frontend must be
> rebuilt because CRA inlines `REACT_APP_API_BASE_URL` at build time).

## 3. Seed the database (one time)

The app has no tables until the DB is seeded. Seeding also enables the pgvector
extension and generates embeddings via OpenAI (needs `OPENAI_API_KEY`).

**Free tier (no Render Shell):** run the seed from your machine against the
database's **External Database URL** (Render dashboard → your DB → "External
Database URL"):

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Point at the remote DB + provide your key for this one run:
export DATABASE_URL="<External Database URL from Render>"   # Windows: set DATABASE_URL=...
export OPENAI_API_KEY="sk-..."                              # Windows: set OPENAI_API_KEY=...
python seed_data.py
```

You should see: `Seeded N characters, ...`. Re-running is safe — it skips if the
DB already has data. Use `RESEED=1 python seed_data.py` to force a full re-seed.

**Paid tier:** uncomment `preDeployCommand: python seed_data.py` in
`render.yaml` and it will seed automatically on each deploy.

## 4. Verify

- Backend health: `https://ff7-backend.onrender.com/health` → `{"status":"ok"}`
- Backend data: `https://ff7-backend.onrender.com/characters` → JSON list
- Open the frontend URL and confirm characters load and a recommendation works.

---

## Notes / gotchas already handled

- **`httpx` pin.** `openai==1.51.0` breaks with `httpx>=0.28` (`proxies` kwarg).
  `requirements.txt` pins `httpx==0.27.2`. Without this the backend crash-loops
  at startup with `TypeError: ... unexpected keyword argument 'proxies'`.
- **Port binding.** Start command uses `--host 0.0.0.0 --port $PORT`; Render
  can't route to the default `127.0.0.1:8000`.
- **DB URL scheme.** `database.py` normalises `postgres://` → `postgresql+psycopg2://`
  so Render's connection string works with SQLAlchemy 2.0.
- **Free instances sleep.** Free web services spin down when idle; the first
  request after a nap takes ~30–60s to wake. Fine for a portfolio link — just
  don't be surprised by the first cold load.

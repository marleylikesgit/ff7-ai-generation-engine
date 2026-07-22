# FF7 Team Synergy AI Generation Engine

AI-powered gear & materia recommender for Final Fantasy VII (1997). Pick 3 party
members, get an OpenAI generated loadout via a
FastAPI + PostgreSQL/pgvector backend.

## How it works

1. **Postgres** stores real character/materia/equipment facts (no hallucinated
   stats) plus a table of curated strategy write-ups with
   pgvector embeddings.
2. When you request a recommendation, the backend embeds your party + playstyle
   query and passes data to OpenAI's chat model.
3. The model returns a structured JSON loadout per character, which the React
   frontend renders.

---------------------------------------------------------------------------------------------

### Run the API

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

---------------------------------------------------------------------------------------------

## 2. Run the frontend 

```bash
cd frontend
npm start
```

---------------------------------------------------------------------------------------------

# FINAL TOUCHES

# ADD A FUNCTION IN WHICH YOU CAN SAY WHERE YOU ARE IN THE GAME
# E.G. 'At Kalm' AND THE AI CAN TELL YOU WHAT TO GET BASED ON WHAT IS AVAILABLE TO YOU
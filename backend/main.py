from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, settings
from models import Character, Materia, Equipment
from schemas import CharacterOut, MateriaOut, EquipmentOut, RecommendRequest, RecommendResponse, GameStageOut
from recommend import generate_recommendation
from game_stages import STAGE_ORDER, STAGE_INFO

app = FastAPI(title="FF7 Team Synergy Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/characters", response_model=list[CharacterOut])
def list_characters(db: Session = Depends(get_db)):
    return db.query(Character).order_by(Character.name).all()


@app.get("/materia", response_model=list[MateriaOut])
def list_materia(db: Session = Depends(get_db)):
    return db.query(Materia).order_by(Materia.name).all()


@app.get("/equipment", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).order_by(Equipment.name).all()


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest, db: Session = Depends(get_db)):
    if len(request.character_names) != 3:
        raise HTTPException(status_code=400, detail="Select exactly 3 characters.")
    try:
        return generate_recommendation(db, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/game-stages", response_model=list[GameStageOut])
def list_game_stages():
    return [
        GameStageOut(id=stage_id, label=info["label"], description=info["description"])
        for stage_id, info in STAGE_INFO.items()
    ]


@app.get("/health")
def health():
    return {"status": "ok"}

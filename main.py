from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/spy_cats/", response_model=schemas.SpyCat)
def create_spy_cat(spy_cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    return crud.create_spy_cat(db=db, spy_cat=spy_cat)


@app.get("/spy_cats/", response_model=List[schemas.SpyCat])
def read_spy_cats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spy_cats = crud.get_spy_cats(db, skip=skip, limit=limit)
    return spy_cats


@app.get("/spy_cats/{cat_id}", response_model=schemas.SpyCat)
def read_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    db_spy_cat = crud.get_spy_cat(db, cat_id=cat_id)
    if db_spy_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return db_spy_cat


@app.patch("/spy_cats/{cat_id}", response_model=schemas.SpyCat)
def update_spy_cat(
    cat_id: int, spy_cat_update: schemas.SpyCatUpdate, db: Session = Depends(get_db)
):
    db_spy_cat = crud.update_spy_cat(db, cat_id=cat_id, spy_cat_update=spy_cat_update)
    if db_spy_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return db_spy_cat


@app.delete("/spy_cats/{cat_id}")
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    db_spy_cat = crud.delete_spy_cat(db, cat_id=cat_id)
    if db_spy_cat is None:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return {"detail": "Spy cat deleted"}


@app.post("/missions/", response_model=schemas.Mission)
def create_mission(mission_data: schemas.MissionCreate, db: Session = Depends(get_db)):
    return crud.create_mission(db=db, mission_data=mission_data)


@app.get("/missions/", response_model=List[schemas.Mission])
def read_missions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    missions = crud.get_missions(db, skip=skip, limit=limit)
    return missions


@app.get("/missions/{mission_id}", response_model=schemas.Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = crud.get_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission


@app.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = crud.delete_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"detail": "Mission  deleted"}



@app.patch("/missions/{mission_id}/targets/{target_id}", response_model=schemas.Target)
def update_target_in_mission(
    mission_id: int,
    target_id: int,
    target_update: schemas.TargetBase,
    db: Session = Depends(get_db),
):
    db_target = crud.update_target(db, target_id=target_id, target_update=target_update)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return db_target


@app.patch("/missions/{mission_id}/assign/{cat_id}", response_model=schemas.Mission)
def assign_cat_to_mission(
    mission_id: int, cat_id: int, db: Session = Depends(get_db)
):
    db_mission = crud.assign_cat_to_mission(db, mission_id=mission_id, cat_id=cat_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission or cat not found")
    return db_mission
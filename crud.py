from sqlalchemy.orm import Session
from models import SpyCat, Mission, Target
from typing import Optional
from schemas import SpyCatCreate, SpyCatUpdate, MissionCreate, TargetCreate


def get_spy_cat(db: Session, cat_id: int):
    return db.query(SpyCat).filter(SpyCat.id == cat_id).first()


def get_spy_cats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SpyCat).offset(skip).limit(limit).all()


def create_spy_cat(db: Session, spy_cat: SpyCatCreate):
    db_spy_cat = SpyCat(
        name=spy_cat.name,
        years_of_experience=spy_cat.years_of_experience,
        breed=spy_cat.breed,
        salary=spy_cat.salary,
    )
    db.add(db_spy_cat)
    db.commit()
    db.refresh(db_spy_cat)
    return db_spy_cat


def update_spy_cat(db: Session, cat_id: int, spy_cat_update: SpyCatUpdate):
    db_spy_cat = get_spy_cat(db, cat_id)
    if db_spy_cat:
        db_spy_cat.salary = spy_cat_update.salary
        db.commit()
        db.refresh(db_spy_cat)
    return db_spy_cat


def delete_spy_cat(db: Session, cat_id: int):
    db_spy_cat = get_spy_cat(db, cat_id)
    if db_spy_cat:
        db.delete(db_spy_cat)
        db.commit()
    return db_spy_cat


def create_mission(db: Session, mission_data: MissionCreate):
    mission = Mission(complete=False)
    db.add(mission)
    db.flush()
    
    for target_data in mission_data.targets:
        target = Target(
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
            complete=target_data.complete,
            mission_id=mission.id
        )
        db.add(target)

    db.commit()
    db.refresh(mission)
    return mission

def get_mission(db: Session, mission_id: int):
    return db.query(Mission).filter(Mission.id == mission_id).first()

def get_missions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Mission).offset(skip).limit(limit).all()

def delete_mission(db: Session, mission_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if mission and not mission.complete:
        db.delete(mission)
        db.commit()
        return True
    return False

def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    if not mission or not cat:
        return None 

    if mission.cat_id is not None:
        return None  
    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission


def update_target(db: Session, target_id: int, target_update: TargetCreate):
    target = db.query(Target).filter(Target.id == target_id).first()
    

    if not target or target.complete:
        return None


    update_data = target_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(target, key, value)

    db.commit()
    db.refresh(target)
    return target

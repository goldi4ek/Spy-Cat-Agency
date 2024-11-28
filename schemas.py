from pydantic import BaseModel, validator
from typing import List, Optional
import requests


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    complete: bool = False


class TargetCreate(TargetBase):
    pass


class Target(TargetBase):
    id: int
    mission_id: int

    class Config:
        orm_mode = True


class MissionBase(BaseModel):
    complete: bool = False


class MissionCreate(MissionBase):
    targets: List[TargetCreate]


class Mission(MissionBase):
    id: int
    cat_id: Optional[int] = None
    targets: List[Target]

    class Config:
        orm_mode = True


class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: int

    @validator("breed")
    def validate_breed(cls, v):
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        breeds = [breed["name"] for breed in response.json()]
        if v not in breeds:
            raise ValueError("This breed is absent in TheCatAPI")
        return v


class SpyCatCreate(SpyCatBase):
    pass


class SpyCatUpdate(BaseModel):
    salary: int


class SpyCat(SpyCatBase):
    id: int
    mission: Optional[Mission] = None

    class Config:
        orm_mode = True

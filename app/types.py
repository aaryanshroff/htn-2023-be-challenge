from typing import TypedDict


class Skill(TypedDict):
    id: int
    skill: str
    rating: int


class User(TypedDict):
    id: int
    name: str
    company: str
    email: str
    phone: str
    skills: list[Skill]

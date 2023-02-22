from typing import List, TypedDict


class Skill(TypedDict):
    id: int
    skill: str
    rating: int


class Event(TypedDict):
    id: int


class User(TypedDict):
    id: int
    name: str
    company: str
    email: str
    phone: str
    skills: List[Skill]
    event: List[Event]

from pydantic import BaseModel
from bson import ObjectId
from datetime import date, datetime

class User(BaseModel):

    _id: ObjectId
    name: str
    dob: date
    address: str
    description: str
    createdAt: datetime
    friends: list
    latitude: float
    longitude: float
    
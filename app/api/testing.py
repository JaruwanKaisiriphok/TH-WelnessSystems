from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

from fastapi import Response
from datetime import date
from fastapi import APIRouter

import json
import os

#router = APIRouter()
router = APIRouter(
    prefix="/Testing",
    tags=["Testing"]
)
# This is a Logon API code comment

# This is a example code comment
# main.py
# This is a 

# FastAPI application that demonstrates how to use
#app = FastAPI()

@router.get('/GetUser',tags=["Customer"])
def index():
    return {'message':'Hello JayKay !!! ...'}

@router.get('/Registrations',tags=["Patients"])
def get_blog():
    return {'message':' All blogs provide'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/Update Patients/{typr}',tags=["Patients"])
def get_blog_type(typr: BlogType):
    return {'message': f'Blog type {typr}'}


@router.get('/Booking/{id}',tags=["Booking"])
def get_blog(id: int):
    return {'message':f'Blog with id {id}'}


d = [
    {"id": 1, "name": "Pele Kanaphon", "date": date.today().isoformat(), "age": 17},
    {"id": 2, "name": "Por Jaruwan", "date": date.today().isoformat(), "age": 52},
]

@router.get("/")
async def MyData():
    # à¸«à¹ˆà¸­ array d à¸”à¹‰à¸§à¸¢ key "data"
    result = {
        "items": d
    }
    json_str = json.dumps(result, indent=4, default=str)
    return Response(content=json_str, media_type="application/json")



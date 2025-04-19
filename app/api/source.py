from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

from fastapi import Response
from datetime import date
from fastapi import APIRouter

import json
import os

router = APIRouter()

router = APIRouter(
    prefix="/sources",
    tags=["Sources"]
)
# This is a Logon API code comment

# This is a example code comment
# main.py
# This is a 

# FastAPI application that demonstrates how to use
#app = FastAPI()

@router.get('/GetUser',tags=["users"])
def index():
    return {'message':'Hello JayKay !!! ...'}

@router.get('/Registrations',tags=["dog"])
def get_blog():
    return {'message':' All blogs provide'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/Update Patients/{typr}',tags=["cats"])
def get_blog_type(typr: BlogType):
    return {'message': f'Blog type {typr}'}


@router.get('/Booking/{id}',tags=["organization"])
def get_blog(id: int):
    return {'message':f'Blog with id {id}'}





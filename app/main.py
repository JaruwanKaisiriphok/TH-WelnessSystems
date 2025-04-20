from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

from fastapi import Response
from datetime import date

import json

from fastapi import FastAPI
from app.api import users,  alerts



app = FastAPI()
#app.include_router(users.router)
app.include_router(alerts.router)
 #app.include_router(users.router)
#app.include_router(appointments.router
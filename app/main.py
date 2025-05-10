from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

from fastapi import Response
from datetime import date

import json

from fastapi import FastAPI
from app.api import users,  alerts, patient, patientid,patient_cre, patient_upd, patient_del,patient_search 


app = FastAPI()
app.include_router(patient_cre.router)
app.include_router(patient_upd.router)
app.include_router(patient_del.router)
app.include_router(patient_search.router)

app.include_router(patientid.router)
app.include_router(patient.router)
app.include_router(users.router)


 #app.include_router(users.router)
#app.include_router(appointments.router


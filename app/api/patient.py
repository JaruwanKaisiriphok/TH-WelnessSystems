
#from fastapi import APIRouter
#from pydantic import BaseModel
#from uuid import uuid4
#from datetime import datetime
#from app.utils.response_code_center import ResponseHandler, ResponseCode

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from supabase import create_client, Client
from app.utils.response_code_center import ResponseHandler, ResponseCode
import os
from dotenv import load_dotenv

#router = APIRouter()
router = APIRouter(

    prefix="/api/v1/patientss",
    tags=["patientss"]
)
# โหลดค่า ENV
load_dotenv()

#router = APIRouter()

# สร้าง Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic model
class Alert(BaseModel):
    alert_type: str
    description: str


# ✅ READ ALL
@router.get("/")
def get_alerts():
    res = supabase.table("patients").select("*").order("id", desc=True).execute()
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_EMPTY, details={})
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(res.data), "patients": res.data}
    )
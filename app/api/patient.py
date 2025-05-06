from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from supabase import create_client, Client
from app.utils.response_code_center import ResponseHandler, ResponseCode
import os
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
import json

router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)

# ตั้งค่า Response เป็น JSON ที่รองรับ UTF-8
class UnicodeJSONResponse(Response):
    media_type = "application/json; charset=utf-8"

    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


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
@router.get("/", response_class=UnicodeJSONResponse)
def get_alerts():
    res = supabase.table("patients").select("*").order("id", desc=True).execute()
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_EMPTY, details={})
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(res.data), "patients": res.data}
    )


# ✅ READ BY NAME
@router.get("/search", response_class=UnicodeJSONResponse)
def search_patients(full_name: str = "", full_name_local: str = "", status: str = ""):
    query = supabase.table("patients").select("*")
    
    if full_name:
        query = query.ilike("full_name", f"{full_name}%")
    if full_name_local:
        query = query.ilike("full_name_local", f"{full_name_local}%")
    if status:
        query = query.ilike("status", f"{status}")        
    
    res = query.execute()
    
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={
            "full_name": full_name,
            "full_name_local": full_name_local,
            "status": status,
        })
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(res.data), "patients": res.data}
    )
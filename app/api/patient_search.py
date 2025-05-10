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
    prefix="/api/v1/patient-search",
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
#class Patient(BaseModel):
    #alert_type: str
    #description: str


# ✅ READ ALL
@router.get("/by all", response_class=UnicodeJSONResponse)
def get():
    res = supabase.table("patients").select("*").order("id", desc=True).execute()
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_EMPTY, details={})
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(res.data), "patients": res.data}
    )


# ✅ READ BY NAME
@router.get("/by name", response_class=UnicodeJSONResponse)
def get(full_name: str = "", status: str = ""):
    query = supabase.table("patients").select("*")
    
    if full_name:
        # 🧠 ใช้ฟิลด์ที่เชื่อม first_name และ last_name ค้นหา
        query = query.filter(f"first_name || ' ' || last_name", "ilike", f"%{full_name}%")
    
    if status:
        query = query.ilike("status", f"{status}")
    
    res = query.execute()
    
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={
            "full_name": full_name,
            "status": status,
        })

    # 🔄 สร้าง full_name ในผลลัพธ์
    patients_with_fullname = []
    for patient in res.data:
        fname = patient.get("first_name", "")
        lname = patient.get("last_name", "")
        full_name_result = f"{fname} {lname}".strip()

        patients_with_fullname.append({
            "full_name": full_name_result,
            "id": patient.get("id"),
            "patientId": patient.get("patientId"),
            "sex": patient.get("sex"),
            "email": patient.get("email"),
            "status": patient.get("status"),
            # ถ้ามี field อื่นๆ ที่อยากแนบก็เพิ่มได้
        })

    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(patients_with_fullname), "patients": patients_with_fullname}
    )
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
    prefix="/api/v1/patients-ID",
    tags=["Patients-ID"]
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

# ✅ READ BY Patient ID
@router.get("/search", response_class=UnicodeJSONResponse)
def search_patients(patientId: str = ""):  
    query = supabase.table("patients").select("*")
    
    if patientId:
        #query = query.filter("{patientId}")
        query = query.filter(f"patientId || ' ' ", "ilike", f"%{patientId}%")
    
    res = query.execute()
    
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={
            "patientId": patientId
        })

    # 🔄 สร้าง full_name ในผลลัพธ์
    patients_with_fullname = []
    for patient in res.data:
        fname = patient.get("first_name", "")
        lname = patient.get("last_name", "")
        full_name_result = f"{fname} {lname}".strip()

        patients_with_fullname.append({
            "id": patient.get("id"),
            "patientId": patient.get("patientId"),
            "full_name": full_name_result,
            "sex": patient.get("sex"),
            "email": patient.get("email"),
            "status": patient.get("status"),
            "religion_id": patient.get("religion_id"),
            "address_id": patient.get("address_id"),
            "profession_id": patient.get("profession_id"),
            "patient_type_id": patient.get("patient_type_id"),
            "payment_id": patient.get("payment_id"),
            "allergy_id": patient.get("allergy_id"),
            "relationship_id": patient.get("relationship_id"),
            "alert_id": patient.get("alert_id"),
            "salesperson_id": patient.get("salesperson_id"),
            "marketing_person_id": patient.get("marketing_person_id"),
            "customer_profile_id": patient.get("customer_profile_id"),
            "source_id": patient.get("source_id"),                                                                        
            # ถ้ามี field อื่นๆ ที่อยากแนบก็เพิ่มได้
            
        })

    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(patients_with_fullname), "patients": patients_with_fullname}
    )
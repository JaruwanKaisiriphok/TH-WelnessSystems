from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from app.utils.response_code_center import ResponseHandler, ResponseCode
import os
from dotenv import load_dotenv
import json
from uuid import UUID
from datetime import datetime
from typing import Optional

router = APIRouter(
    prefix="/api/v1/patient-update",
    tags=["Patients"]
)

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

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Patient(BaseModel):
    first_name: str
    last_name: str
    first_name_local: str
    last_name_local: str
    sex: str
    birth_date: datetime
    religion_id: Optional[str]
    address_id: Optional[str]
    profession_id: Optional[str]
    patient_type_id: Optional[str]
    telephone: str
    work_phone: str
    social_security_id: str
    email: str
    line_id: str
    facebook: str
    whatsapp: str
    payment_id: Optional[str]
    payment_status: str
    allergy_id: Optional[str]
    allergy_note: str
    contact_first_name: str
    contact_last_name: str
    contact_phone1: str
    contact_phone2: str
    relationship_id: Optional[str]
    alert_id: Optional[str]
    salesperson_id: Optional[str]
    marketing_person_id: Optional[str]
    customer_profile_id: Optional[str]
    source_id: Optional[str]
    created_at: datetime
    status: str
    full_name: str
    full_name_local: str
    locations_id: int

@router.put("/", response_class=UnicodeJSONResponse)
def put(patientId: str, patients: Patient):
    try:
        updated = {
            "first_name": patients.first_name,
            "last_name": patients.last_name,
            "first_name_local": patients.first_name_local,
            "last_name_local": patients.last_name_local,
            "sex": patients.sex,
            "birth_date": patients.birth_date.isoformat(),
            "religion_id": patients.religion_id or None,
            "address_id": patients.address_id or None,
            "profession_id": patients.profession_id or None,
            "patient_type_id": patients.patient_type_id or None,
            "telephone": patients.telephone,
            "work_phone": patients.work_phone,
            "social_security_id": patients.social_security_id,
            "email": patients.email,
            "line_id": patients.line_id,
            "facebook": patients.facebook,
            "whatsapp": patients.whatsapp,
            "payment_id": patients.payment_id or None,
            "payment_status": patients.payment_status,
            "allergy_id": patients.allergy_id or None,
            "allergy_note": patients.allergy_note,
            "contact_first_name": patients.contact_first_name,
            "contact_last_name": patients.contact_last_name,
            "contact_phone1": patients.contact_phone1,
            "contact_phone2": patients.contact_phone2,
            "relationship_id": patients.relationship_id or None,
            "alert_id": patients.alert_id or None,
            "salesperson_id": patients.salesperson_id or None,
            "marketing_person_id": patients.marketing_person_id or None,
            "customer_profile_id": patients.customer_profile_id or None,
            "source_id": patients.source_id or None,
            "created_at": datetime.utcnow().isoformat(),
            "status": patients.status,
            "full_name": patients.full_name,
            "full_name_local": patients.full_name_local,
            "locations_id": patients.locations_id,
        }

        res = supabase.table("patients").update(updated).eq("patientId", str(patientId)).execute()

        if not res.data:
            return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={"patientId": str(patientId)})

        return ResponseHandler.success(
            message=ResponseCode.SUCCESS_UPDATED[1],
            data={"patients": res.data[0]}
        )
    except Exception as e:
        print("❌ Exception occurred:", e)
        raise HTTPException(status_code=500, detail=str(e))
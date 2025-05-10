from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from app.utils.response_code_center import ResponseHandler, ResponseCode
import os
from dotenv import load_dotenv
from datetime import datetime
from uuid import UUID
import json
from typing import Optional
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/api/v1/patient-create", tags=["Patients"])

class UnicodeJSONResponse(Response):
    media_type = "application/json; charset=utf-8"
    def render(self, content: any) -> bytes:
        return json.dumps(content, ensure_ascii=False).encode("utf-8")

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is not set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Patient(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    first_name_local: str
    last_name_local: str
    sex: str
    birth_date: datetime
    religion_id: str
    address_id: str
    profession_id: str
    patient_type_id: str
    telephone: str
    work_phone: str
    social_security_id: str
    email: str
    line_id: str
    facebook: str
    whatsapp: str
    payment_id: str
    payment_status: str
    allergy_id: str
    allergy_note: str
    contact_first_name: str
    contact_last_name: str
    contact_phone1: str
    contact_phone2: str
    relationship_id: str
    alert_id: str
    salesperson_id: str
    marketing_person_id: str
    customer_profile_id: str
    source_id: str
    created_at: datetime
    patientId: str
    status: str
    patient_pic: Optional[str]  # ✅ รองรับ base64 string
    full_name: str
    full_name_local: str
    locations_id: int

#JSON Request body
"""
{
  "first_name": "Jaruwan-1001",
  "last_name": "Kaisiriphok",
  "first_name_local": "จารุวรรณ",
  "last_name_local": "ไกรสิริโภค",
  "sex": "female",
  "birth_date": "2025-05-08T12:31:05.813Z",
  "religion_id": "7b617db2-87c3-499b-8492-b34b095c5105",
  "address_id": "7b617db2-87c3-499b-8492-b34b095c5103",
  "profession_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "patient_type_id": "7b617db2-87c3-499b-8492-b34b095c5102",
  "telephone": "66899962903",
  "work_phone": "",
  "social_security_id": "",
  "email": "jaruwan.kaisiriphok@gmail.com",
  "line_id": "",
  "facebook": "",
  "whatsapp": "",
  "payment_id": "",
  "payment_status": "",
  "allergy_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "allergy_note": "",
  "contact_first_name": "Emergency contact first name.",
  "contact_last_name": "Emergency contact last name.",
  "contact_phone1": "Emergency contact contact number.-1",
  "contact_phone2": "Secondary emergency contact number.-2",
  "relationship_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "alert_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "salesperson_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "marketing_person_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "customer_profile_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "source_id": "7b617db2-87c3-499b-8492-b34b095c5101",
  "created_at": "2025-05-08T11:28:32.324Z",
  "status": "Active",
  "full_name": "Jaruwan Kaisiriphok",
  "full_name_local": "จารุวรรณ ไกรสิริโภค",
  "locations_id": 10
}
"""


@router.post("/", response_class=UnicodeJSONResponse)
def post(patient: Patient):
    try:
        data = jsonable_encoder(patient)
        data["created_at"] = datetime.utcnow().isoformat()

        # Clean "" to None
        cleaned_data = {
            k: (None if v == "" else v)
            for k, v in data.items()
        }

        print("Insert data:", cleaned_data)

        res = supabase.table("patients").insert(cleaned_data).execute()

        # ✅ Updated error check
        if not res.data:
            raise HTTPException(status_code=400, detail="Insert failed or no data returned.")

        return ResponseHandler.success(
            message=ResponseCode.SUCCESS_REGISTERED[1],
            data={"patient": res.data[0]}
        )

    except Exception as e:
        print("Exception:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


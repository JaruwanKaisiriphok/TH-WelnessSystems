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


# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Alert(BaseModel):
    alert_type: str
    description: str

@router.get("/by-id", response_class=UnicodeJSONResponse)
def get_patient_by_id(patientId: str):
    query = supabase.table("patients").select("""
        *,
        religions(religion_name),
        professions(profession_name),
        addresses(street, city, state, country),
        patient_types(type_name),
        relationships(relationship_name),
        alerts(alert_type),
        salespersons(name),
        marketing_persons(name),
        customer_profiles(medical_history),
        sources(source_name)
    """).eq("patientId", patientId)

    res = query.execute()

    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={"patientId": patientId})

    p = res.data[0]  # Get the first matched patient

    result = {
    "id": p["id"],
    "patientId": p.get("patientId"),
    "full_name": f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
    "religion_name": p["religions"]["religion_name"] if p.get("religions") else None,
    "profession": p["professions"]["profession_name"] if p.get("professions") else None,
    "address_city": p["addresses"]["city"] if p.get("addresses") else None,
    "patient_type": p["patient_types"]["type_name"] if p.get("patient_types") else None,
    "relationship": p["relationships"]["relationship_name"] if p.get("relationships") else None,
    "alert_type": p["alerts"]["alert_type"] if p.get("alerts") else None,
    "salesperson": p["salespersons"]["name"] if p.get("salespersons") else None,
    "marketer": p["marketing_persons"]["name"] if p.get("marketing_persons") else None,
    "source": p["sources"]["source_name"] if p.get("sources") else None,
}


    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data=result
    )

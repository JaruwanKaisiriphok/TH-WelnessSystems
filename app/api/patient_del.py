from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from app.utils.response_code_center import ResponseHandler, ResponseCode
import os
from dotenv import load_dotenv
import json
from uuid import UUID
from datetime import datetime

router = APIRouter(
    prefix="/api/v1/patient-delete",
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

@router.delete("/", response_class=UnicodeJSONResponse)
def delete(patientId: str):
    try:
        print(f"🗑️ Deleting patientId: {patientId}")
        res = supabase.table("patients").delete().eq("patientId", str(patientId)).execute()

        if not res.data:
            return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={"patientId": str(patientId)})

        return ResponseHandler.success(
            message=f"Patient with patientId {patientId} deleted.",
            data={"patientId": str(patientId)}
        )
    except Exception as e:
        print("❌ Exception during delete:", e)
        raise HTTPException(status_code=500, detail=str(e))

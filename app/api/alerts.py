
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

    prefix="/api/v1/alearts",
    tags=["alerts"]
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

# ✅ CREATE
@router.post("/", tags=["alert"])
def create_alert(alert: Alert):
    data = {
        "alert_type": alert.alert_type,
        "description": alert.description,
        "created_at": datetime.utcnow().isoformat()
    }
    res = supabase.table("alerts").insert(data).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)

    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_REGISTERED[1],
        data={"alert": res.data[0]}
    )

# ✅ READ ALL
@router.get("/", tags=["alert"])
def get_alerts():
    res = supabase.table("alerts").select("*").order("created_at", desc=True).execute()
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_EMPTY, details={})
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"total": len(res.data), "alerts": res.data}
    )

# ✅ READ BY ID
@router.get("/{alert_id}", tags=["alert"])
def get_alert(alert_id: UUID):
    res = supabase.table("alerts").select("*").eq("id", str(alert_id)).execute()
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={"alert_id": str(alert_id)})
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={"alert": res.data[0]}
    )

# ✅ UPDATE
@router.put("/{alert_id}")
def update_alert(alert_id: UUID, alert: Alert):
    updated = {
        "alert_type": alert.alert_type,
        "description": alert.description,
        "created_at": datetime.utcnow().isoformat()  # หากคุณมี updated_at ให้ใช้ตรงนี้
    }
    res = supabase.table("alerts").update(updated).eq("id", str(alert_id)).execute()
    if not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={"alert_id": str(alert_id)})
    
    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_UPDATED[1],
        data={"alert": res.data[0]}
    )

# ✅ DELETE
@router.delete("/{alert_id}")
def delete_alert(alert_id: UUID):
    res = supabase.table("alerts").delete().eq("id", str(alert_id)).execute()
    if res.status_code != 200 or not res.data:
        return ResponseHandler.error(*ResponseCode.USER_NOT_FOUND, details={"alert_id": str(alert_id)})

    return ResponseHandler.success(
        message=f"Alert with id {alert_id} deleted.",
        data={"alert_id": str(alert_id)}
    )




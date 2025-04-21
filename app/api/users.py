from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.response_code_center import ResponseHandler, ResponseCode

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

# Pydantic model สำหรับ user
class User(BaseModel):
    id: int
    name: str
    email: str

# Fake database (จำลองข้อมูล)
#fake_users_db = [
#    {"id": 1, "name": "Alice", "email": "alice@example.com"},
#    {"id": 2, "name": "Bob", "email": "bob@example.com"}
#]
from uuid import uuid4
from datetime import datetime

fake_users_db = [
    {
        "id": 1,
        "user_id": 1,
        "username": "alice123",
        "full_name": "Alice Wonderland",
        "phone_numbe": "0812345678",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": 2,
        "user_id": 2,
        "username": "bob456",
        "full_name": "Bob Builder",
        "phone_numbe": "0823456789",
        "role": "user",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
]

# ✅ GET all users
@router.get("/", tags=["alert"])
def get_users():
    if not fake_users_db:
        return ResponseHandler.error(
            *ResponseCode.USER_EMPTY,
            details={}
        )

    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_RETRIEVED[1],
        data={
            "total": len(fake_users_db),
            "users": fake_users_db
        }
    )

# ✅ GET user by ID
@router.get("/{user_id}")
def get_user_by_id(user_id: int):    
    user = next((u for u in fake_users_db if u["id"] == user_id), None)

    if user:
        return ResponseHandler.success(
            message=ResponseCode.SUCCESS_RETRIEVED[1],
            data={"user": user}
        )

    return ResponseHandler.error(
        *ResponseCode.USER_NOT_FOUND,
        details={"user_id": user_id}
    )

# ✅ POST user (สร้างผู้ใช้ใหม่)
# Pydantic model
from pydantic import BaseModel, EmailStr
# ✅ Pydantic model (เพิ่ม email)
class User(BaseModel):
    id: int
    name: str
    email: EmailStr

@router.post("/")
def create_user(user: User):
    # ตรวจสอบว่าผู้ใช้มีอยู่แล้วหรือไม่ (id หรือ email ซ้ำ)
    if any(u["id"] == user.id or u["email"] == user.email for u in fake_users_db):
        return ResponseHandler.error(
            *ResponseCode.DB_DUPLICATE_ENTRY,
            details={"user_id": user.id, "email": user.email}
        )

    # เพิ่มผู้ใช้ใหม่
    fake_users_db.append(user.dict())

    return ResponseHandler.success(
        message=ResponseCode.SUCCESS_REGISTERED[1],
        data={"user": user.dict()}
    )


# ✅ PUT user by ID (อัปเดตข้อมูลผู้ใช้)
class User(BaseModel):
    id: int
    name: str
@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    for idx, u in enumerate(fake_users_db):
        if u["id"] == user_id:
            fake_users_db[idx] = user.dict()
            return ResponseHandler.success(
                message=ResponseCode.SUCCESS_UPDATED[1],
                data={"user": user.dict()}
            )

    return ResponseHandler.error(
        *ResponseCode.DB_DUPLICATE_ENTRY,  # หรือจะสร้าง ResponseCode.USER_NOT_FOUND ก็ได้
        details={"user_id": user_id}
    )

# ✅ DELETE user by ID  
@router.delete("/{user_id}")
def delete_user(user_id: int):
    global fake_users_db

    # ตรวจสอบว่าผู้ใช้นี้มีอยู่หรือไม่
    existing_user = next((u for u in fake_users_db if u["id"] == user_id), None)

    if not existing_user:
        return ResponseHandler.error(*ResponseCode.DB_DUPLICATE_ENTRY, details={"user_id": user_id})

    # ลบ user และอัปเดต fake_users_db
    fake_users_db = [u for u in fake_users_db if u["id"] != user_id]

    return ResponseHandler.success(
        message=f"User with id {user_id} deleted.",
        data={"user_id": user_id}
    )
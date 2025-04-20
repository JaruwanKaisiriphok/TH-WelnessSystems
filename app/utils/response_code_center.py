from fastapi.responses import JSONResponse
from typing import Optional, Dict

#from app.api import users,  alerts

# ✅ รวบรวม Error และ Success Code
class ResponseCode:
    # Authentication Errors
    AUTH_INVALID_CREDENTIALS = ("AUTH_001", "Invalid credentials provided.")
    AUTH_UNAUTHORIZED = ("AUTH_002", "Unauthorized access.")

    # Validation Errors
    VALID_MISSING_FIELDS = ("VALID_001", "Missing required fields.")
    VALID_INVALID_EMAIL = ("VALID_002", "Invalid email format.")

    # Database Errors
    DB_CONNECTION_FAILED = ("DB_001", "Failed to connect to database.")
    DB_DUPLICATE_ENTRY = ("DB_002", "Duplicate entry found.")
   

    # API Errors
    API_NOT_FOUND = ("API_001", "Endpoint not found.")

    # System Errors
    SYS_INTERNAL_ERROR = ("SYS_001", "Internal server error.")

    # Success Codes
    SUCCESS_REGISTERED = ("SUCCESS_001", "User registered successfully.")
    SUCCESS_UPDATED = ("SUCCESS_002", "Data updated successfully.")
    SUCCESS_RETRIEVED = ("SUCCESS_003", "Data retrieved successfully.")

    # User error
    USER_NOT_FOUND = ("USER_001", "User not found.")
    USER_EMPTY = ("USER_002", "No users found.")

# ✅ Handler สำหรับสร้าง Response JSON
class ResponseHandler:

    @staticmethod
    def success(message: str, data: Optional[dict] = None):
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": message,
                "data": data or {}
            }
        )
    @staticmethod
    def error(code: str, message: str, details: Optional[Dict] = None, status_code: int = 400):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "error_code": code,
                "message": message,
                "details": details or {}
            }
        )

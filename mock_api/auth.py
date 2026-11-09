from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Demo users and tokens
TOKENS = {
    "emp1": {
        "user_id": "EMP001",
        "role": "employee"
    },
    "emp2": {
        "user_id": "EMP002",
        "role": "employee"
    },
    "emp3": {
        "user_id": "EMP003",
        "role": "employee"
    },
    "emp4": {
        "user_id": "EMP004",
        "role": "employee"
    },
    "man": {
        "user_id": "MGR001",
        "role": "manager"
    }
}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = TOKENS.get(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


def require_manager(
    user: dict = Depends(get_current_user)
):
    if user["role"] != "manager":
        raise HTTPException(
            status_code=403,
            detail="Only managers can approve leave requests"
        )

    return user
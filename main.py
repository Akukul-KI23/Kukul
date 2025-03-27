from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict

app = FastAPI()

fake_users_db = {
    "admin_token": {"role": "admin"},
    "user_token": {"role": "user"},
    "guest_token": {"role": "guest"},
}

permissions = {
    "admin": ["create", "read", "update", "delete"],
    "user": ["read", "update"],
    "guest": ["read"],
}

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = fake_users_db.get(token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return user

def role_required(required_role: str):
    def role_wrapper(current_user: Dict = Depends(get_current_user)):
        if current_user['role'] != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return current_user

    return role_wrapper

@app.post("/resource")
def create_resource(user: Dict = Depends(role_required("admin"))):
    return {"message": "Resource created"}

@app.get("/resource")
def read_resource(user: Dict = Depends(role_required("guest"))):
    return {"message": "Resource data"}

@app.put("/resource")
def update_resource(user: Dict = Depends(role_required("user"))):
    return {"message": "Resource updated"}

@app.get("/protected_resource")
def protected_resource(user: Dict = Depends(role_required("user"))):
    return {"message": "Access granted to protected resource"}

@app.get("/admin_resource")
def admin_resource(user: Dict = Depends(role_required("admin"))):
    return {"message": "Access granted to admin resource"}

# uvicorn main:app --reload

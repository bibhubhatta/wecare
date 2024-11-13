from fastapi import FastAPI, HTTPException
from pantrysoft_authenticator import get_php_session_id
from pydantic import BaseModel

app = FastAPI()


class AuthRequest(BaseModel):
    username: str
    password: str


@app.post("/authenticate")
async def authenticate(auth_request: AuthRequest):
    try:
        session_id = get_php_session_id(auth_request.username, auth_request.password)
        return {"PHPSESSID": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

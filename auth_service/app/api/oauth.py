from fastapi import APIRouter, Request
from requests_oauthlib import OAuth2Session
import os

router = APIRouter(prefix="/oauth", tags=["OAuth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8000/oauth/google/callback"

@router.get("/google/login")
def google_login():
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI, scope=["openid", "email", "profile"])
    auth_url, _ = google.authorization_url("https://accounts.google.com/o/oauth2/auth")
    return {"auth_url": auth_url}

@router.get("/google/callback")
def google_callback(request: Request):
    code = request.query_params.get("code")
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI)
    token = google.fetch_token(
        "https://oauth2.googleapis.com/token",
        client_secret=GOOGLE_CLIENT_SECRET,
        code=code
    )
    user_info = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    return {"user": user_info}

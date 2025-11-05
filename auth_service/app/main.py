from fastapi import FastAPI
from app.api import routes_auth
from app.db import models, database
from app.api import oauth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Auth Service")
app.include_router(routes_auth.router)
app.include_router(oauth.router)

@app.get("/")
def root():
    return {"message": "Auth Service Running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
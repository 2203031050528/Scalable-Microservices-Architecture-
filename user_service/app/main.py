from fastapi import FastAPI
from app.routes import user_routes, team_routes
from app.core.db import engine, Base

app = FastAPI(title="User Service")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(user_routes.router)
app.include_router(team_routes.router)

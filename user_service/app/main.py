from fastapi import FastAPI
from app.routes import user_routes, team_routes
from app.core.db import engine, Base

app = FastAPI(title="User Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_routes.router)
app.include_router(team_routes.router)

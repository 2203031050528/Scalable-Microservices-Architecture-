from fastapi import FastAPI
from app.routes import project_routes, task_routes
from app.core.db import engine, Base

app = FastAPI(title="Project Service")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    
app.include_router(project_routes.router)
app.include_router(task_routes.router)

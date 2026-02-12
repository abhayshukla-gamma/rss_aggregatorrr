from fastapi import FastAPI
from app.models import feed , item
from app.core.database import Base,engine
from app.routers import feed_router
from app.services.scheduler_service import start_scheduler


app = FastAPI()

@app.on_event("startup")
def startup_event():
    start_scheduler()

app.include_router(feed_router.router)
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
 # to tell python to create table in a database 

# @app.get("/")
# def root() :
#     return {"status":"server is running "}

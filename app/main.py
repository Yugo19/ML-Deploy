from fastapi import FastAPI
from app.apis import main_router
from fastapi.middleware.cors import CORSMiddleware
from .config import *

app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    

app.include_router(main_router.router, prefix="/api1", tags=["api1"])

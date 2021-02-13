from fastapi import FastAPI
from routers import classify, metrics
import json
import toml
import uvicorn


app = FastAPI()
app.include_router(classify.router)
app.include_router(metrics.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

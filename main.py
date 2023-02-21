"""
Entry point for the backend service/API. 
Contains connections to MongoDB and Kafka
Serves index.html (not sure how to completely move that to UI service
or if I even can/should.)
"""

import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from src.api import router

# Set up the FastAPI entrypoint
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(router.sample_router)
templates = Jinja2Templates(directory="./templates")

# Define endpoints
@app.get('/')
async def root(request: Request):
    """ Main endpoint """
    return templates.TemplateResponse("index.html", {"request": request})

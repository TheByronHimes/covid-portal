import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

# Import Username & Password from container env vars
DB_USERNAME = os.environ["db_username"]
DB_PASSWORD = os.environ["db_password"]

# Create connection to DB
client = MongoClient(
    host="mongodb://mongo:27017", username=DB_USERNAME, password=DB_PASSWORD
)

# Set up the FastAPI entrypoint
app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

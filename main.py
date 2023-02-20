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
from svcKafka.kafkaservice import KafkaService
from src.api import router

# Import DB Username & Password from container env vars
DB_USERNAME = os.environ["db_username"]
DB_PASSWORD = os.environ["db_password"]

# TODO: move this to a proper config file or something
TOPIC_NAME = 'nutopic'
BOOTSTRAP_SERVERS = ['broker:29092']
CLIENT_ID = 'client1'

# Create connection to DB
client = MongoClient(
    host="mongodb://db:27017", username=DB_USERNAME, password=DB_PASSWORD
)


# Set up the FastAPI entrypoint
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(router.sample_router)
templates = Jinja2Templates(directory="./templates")

# Set up kafka service (currently only able to produce)
ks = KafkaService(BOOTSTRAP_SERVERS, CLIENT_ID)
ks.add_new_topic(TOPIC_NAME)
#x = ks.produce_simple_message(TOPIC_NAME, 'test message')

#consumer = KafkaConsumer(group_id=None, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset='earliest')#,request_timeout_ms=5000, session_timeout_ms=3000)
#consumer.subscribe(topics=[TOPIC_NAME]) 


# Define endpoints
@app.get('/')
async def root(request: Request):
    """ Main endpoint """
    return templates.TemplateResponse("index.html", {"request": request})

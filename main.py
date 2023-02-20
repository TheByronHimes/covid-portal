"""
Entry point for the backend service/API. 
Contains connections to MongoDB and Kafka
Serves index.html (not sure how to completely move that to UI service
or if I even can/should.)
"""

import os
from json import dumps
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from svcKafka.kafkaservice import KafkaService

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
templates = Jinja2Templates(directory="./templates")

# Set up kafka service (currently only able to produce)
ks = KafkaService(BOOTSTRAP_SERVERS, CLIENT_ID)
ks.add_new_topic(TOPIC_NAME)
#x = ks.produce_simple_message(TOPIC_NAME, 'test message')

#consumer = KafkaConsumer(group_id=None, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset='earliest')#,request_timeout_ms=5000, session_timeout_ms=3000)
#consumer.subscribe(topics=[TOPIC_NAME]) 

def findSample(*args):
    raise NotImplementedError


def addSample(*args):
    raise NotImplementedError


def updateSample(*args):
    raise NotImplementedError


@app.get('/sample/{access_token}', status_code=200)
def get_sample(access_token: str):
    """ Handle GET req and return test sample information if found """
    access_token = access_token.strip()
    data_to_return, status_code = findSample(access_token)
    # TODO: get rid of the approach where we call some other function
    # TODO: replace w/ DAO/DTO pattern approach
    return data_to_return


@app.post('/sample', status_code=201)
def post_sample():
    """
    Handle POST req: 
        1. Insert new data
        2. Return sample_id and access_token
    """
    req = dict()
    data_to_return = addSample(
        req['patient_pseudonym'],
        req['submitter_email'],
        req['collection_date']
    )
    return data_to_return


@app.patch('/sample', status_code=204)
def update_sample():
    """ 
    Handle PATCH req: 
        1. Find sample with matching access_token 
        2. Update sample 
        3. Return updated sample
    """
    req = dict()
    data_to_return = updateSample(
        req['access_token'],
        req['status'],
        req['test_result'],
        req['test_date']
    )
    return data_to_return


# Define endpoints
@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

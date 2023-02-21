"""
Desc: Module that handles the main API functionality.
Contents:
    - findSample()
    - updateSample()
    - get_sample()
    - post_sample()
    - update_sample()
"""

import secrets
import os
from typing import Dict
from fastapi import APIRouter
from pymongo import MongoClient
from .deps import make_access_token, sample_id
from .dao import PcrTest, UpdatePcrTest, MongoDao
from .kafkaservice import KafkaService

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
mdao = MongoDao(PcrTest, client['db']['samples'], '_id')


# Set up kafka service (currently only able to produce)
ks = KafkaService(BOOTSTRAP_SERVERS, CLIENT_ID)
ks.add_new_topic(TOPIC_NAME)
#x = ks.produce_simple_message(TOPIC_NAME, 'test message')

#consumer = KafkaConsumer(group_id=None, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset='earliest')#,request_timeout_ms=5000, session_timeout_ms=3000)
#consumer.subscribe(topics=[TOPIC_NAME]) 


# Helper functions that might get moved or replaced by something else.
def findSample(access_token: str) -> PcrTest:
    return mdao.find_one({'access_token': access_token})

def updateSample(access_token: str, new_data: PcrTest) -> PcrTest:
    result = mdao.update_one(
        {'access_token': access_token},
        new_data
    )
    return result


# Establish routes
sample_router = APIRouter()
@sample_router.get('/sample/{access_token}', status_code=200)
def get_sample(access_token: str):
    """ 
    Search for a test sample matching the access token.
    Handle GET req:
        1. Return test sample information if found 
    """
    access_token = access_token.strip()
    sample = findSample(access_token)
    data_to_return = sample.to_dict([
        'patient_pseudonym',
        'submitter_email',
        'collection_date',
        'status',
        'test_result',
        'test_date'
    ])
    return data_to_return


@sample_router.post('/sample', status_code=201)
def post_sample(data: PcrTest):
    """
    Upload a new sample.
    Handle POST req: 
        1. Insert new data
        2. Return sample_id and access_token
    """
    data.access_token = make_access_token()
    data.sample_id = secrets.randbits(40)
    record_id = mdao.insert_one(data)
    sample = mdao.find_one({'_id': record_id})
    data_to_return = sample.to_dict([
        'sample_id',
        'access_token'
    ])

    return data_to_return


@sample_router.patch('/sample', status_code=201)
def update_sample(data: UpdatePcrTest):
    """
    Update a test sample with results.
    Handle PATCH req: 
        1. Find sample with matching access_token 
        2. Update sample 
        3. Return updated sample
    """
    sample = findSample(data.access_token)
    sample.status = data.status
    sample.test_result = data.test_result
    sample.test_date = data.test_date

    result = updateSample(data.access_token, sample)
    
    return result.to_dict()

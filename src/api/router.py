import secrets
import os
from typing import Dict
from fastapi import APIRouter
from pymongo import MongoClient
from .deps import make_access_token
from .dao import PcrTest, MongoDao

# Import DB Username & Password from container env vars
DB_USERNAME = os.environ["db_username"]
DB_PASSWORD = os.environ["db_password"]

# Create connection to DB
client = MongoClient(
    host="mongodb://db:27017", username=DB_USERNAME, password=DB_PASSWORD
)

sample_router = APIRouter()
mdao = MongoDao(PcrTest, client['db']['samples'], '_id')

def findSample(access_token: str) -> Dict:
    return mdao.find_one({'access_token': access_token})

def updateSample(*args):
    raise NotImplementedError

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
    #data_to_return, status_code = findSample(access_token)
    # TODO: get rid of the approach where we call some other function
    # TODO: replace w/ DAO/DTO pattern approach
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


@sample_router.patch('/sample', status_code=204)
def update_sample():
    """
    Update a test sample with results.
    Handle PATCH req: 
        1. Find sample with matching access_token 
        2. Update sample 
        3. Return updated sample
    """
    raise NotImplementedError
    data_to_return = updateSample(
        req['access_token'],
        req['status'],
        req['test_result'],
        req['test_date']
    )
    return data_to_return

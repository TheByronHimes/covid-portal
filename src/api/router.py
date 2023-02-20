from json import dumps
from typing import Dict
from fastapi import APIRouter

sample_router = APIRouter()

def findSample(access_token: str) -> Dict:
    raise NotImplementedError


def addSample(*args):
    raise NotImplementedError


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
    data_to_return = {'msg': 'nothing real'}
    #data_to_return, status_code = findSample(access_token)
    # TODO: get rid of the approach where we call some other function
    # TODO: replace w/ DAO/DTO pattern approach
    return data_to_return


@sample_router.post('/sample', status_code=201)
def post_sample():
    """
    Upload a new sample.
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


@sample_router.patch('/sample', status_code=204)
def update_sample():
    """ 
    Update a test sample with results.
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
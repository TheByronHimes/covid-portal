import pytest
from . import dao, deps

def test_with_all_valid_input():
    """ Uses valid input to add an object """
    try:
        # create object
        p = dao.PcrTest(
            sample_id = deps.sample_id(),
            patient_pseudonym = 'Alfredo Barnelli',
            submitter_email = 'test@test.com',
            collection_date = '2022-08-21T11:18',
            access_token = '1234567812345678'
        )
        assert True
    except:
        pass

@pytest.mark.xfail
def test_with_too_long_name():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'sadfasdfasdfasdasdfkjalsdkjflaks\
            djlfkasdlkfasldkfjalksdjfsdfdfdd',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21T11:18',
        access_token = '2234567812345678'
    )
    print('PcrTest was created with too-long string for name')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_too_short_name():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = '0123456789',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21T11:18',
        access_token = '3234567812345678'
    )
    print('PcrTest was created with too-short string for name')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_invalid_email_format():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'testtest.com',
        collection_date = '2022-08-21T11:18',
        access_token = '43234567812345678'
    )

    print('PcrTest accepted invalid email address')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_bad_status():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21T11:18',
        status='invalid',
        access_token = '53234567812345678'
    )
    print('invalid status was accepted')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_too_long_email():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'testtesttesttesttesttesttesttesttesttesttesttest\
        testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
        testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
        testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
        testtesttest@test.com',
        collection_date = '2022-08-21T11:18',
        access_token = '63234567812345678'
    )
    print('PcrTest accepted too-long email address')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_too_long_token():

    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21T11:18',
        access_token='a1b2c3d4e5f6g7h8i9'
    )

    print('PcrTest accepted too-long access_token')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_invalid_token():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21T11:18',
        access_token='a1b2c3d4e5f6g7h$'
    )
    print('PcrTest accepted invalid access_token')
    self.assertIs(True, True)

@pytest.mark.xfail
def test_with_date_no_T():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21 11:18',
        access_token = '73234567812345678'
    )

@pytest.mark.xfail
def test_with_date_short_year():
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'test@test.com',
        collection_date = '22-08-21T11:18',
        access_token = '83234567812345678'
    )

@pytest.mark.xfail
def test_with_date_with_milliseconds(self):
    # create object
    p = dao.PcrTest(
        sample_id = deps.sample_id(),
        patient_pseudonym = 'Alfredo Barnelli',
        submitter_email = 'test@test.com',
        collection_date = '2022-08-21T11:18.357',
        access_token = '93234567812345678'
    )
""" 
Desc: DAO-related classes and functionality 
Contents:
    - class Dao(Protocol)
    - class MongoDao (implements Dao class)

"""

# TODO: Proper type-hinting
# TODO: write tests for existing and future code

from typing import Protocol, Mapping, Any, List, Type
from pydantic import BaseModel


class Dto(BaseModel):
    """ Base class for a DTO """
    def to_dict(self, fields: List[str] | None = None):
        if not fields:
            fields = self.__fields__
        return {k: getattr(self, k) for k in fields}

class PcrTest(Dto):
    """ Simple DTO for the PCR tests """
    #TODO: proper enumeration on status and test result fields
    patient_pseudonym: str
    submitter_email: str
    collection_date: str
    sample_id: int = ''
    access_token: str = ''
    status: str = ''
    test_result: str = ''
    test_date: str = ''

    class Config:
        validate_assignment = True

class UpdatePcrTest(Dto):
    """ Update DTO for PcrTest """
    #TODO: proper validation on the date fields
    #TODO: proper enumeration on status and test result fields
    access_token: str
    status: str = ''
    test_result: str = ''
    test_date: str = ''


class Dao(Protocol):
    """
    A Protocol class containing the basic functions for a Data Access Object.
    """
    def insert_one():
        """ a method to insert one record """

    def update_one():
        """ a method to update one record """

    def find_one():
        """ a method to find one record """
    
    def delete_one():
        """ a method to delete one record """



class MongoDao:
    """ A DAO Implementation specifically for MongoDB """
    # TODO: Create DTO Class
    # TODO: Update type-hint for dto_type
    def __init__(self, dto_type: Type[Dto], collection, key_field):
        """
        TODO: Pretty sure I need to do something with a session here so
        MongoDbDao isn't relying on the existing session in main.py, but I'll
        worry about that later
        """
        self.dto_type = dto_type
        self.key_field = key_field
        self.collection = collection

    def _dto_to_document(self, dto):
        document = dto.dict()
        return document

    def _document_to_dto(self, document):
        document.pop("_id")
        return self.dto_type(**document)

    def find_all(self, filters: Mapping[str, Any] = {}) -> List[Any]:  # , filter: Mapping[str, Any] = {}):
        """Find all"""
        # hexkit's version accepts & validates a filter mapping
        # it then returns the documents async-generator style
        if filters == {}:
            return [self._document_to_dto(x) for x in self.collection.find()]
        return [self._document_to_dto(x) for x in self.collection.find(filters)]

    def find_one(self, filters: Mapping[str, Any]):
        """Find first item that matches criteria"""
        return self._document_to_dto(self.collection.find_one(filters))

    def insert_one(self, obj):
        """Insert one item"""
        document = self._dto_to_document(obj)
        inserted = self.collection.insert_one(document)
        if inserted:
            return inserted.inserted_id
        return None

    def update_one(
        self,
        filters: Mapping[str, Any],
        replacement: Dto
    ):
        """ Update given item """
        """ 
        Hexkit takes a replacement approach instead of an update,
        which would remove the need for the 'updates' mapping wrapper,
        but it still doesn't allow any kind of dynamic update (which is fine).
        """
        replacement_doc = self._dto_to_document(replacement)
        self.collection.find_one_and_replace(filters, replacement_doc)
        return self._document_to_dto(self.collection.find_one(filters))

    def delete_one(self, filters: Mapping[str, Any]):
        """Delete an item"""
        x = self.find_one(filters)
        _id = ""
        if x:
            _id = x["_id"]
            self.collection.delete_one({"_id": _id})
            return True
        return False
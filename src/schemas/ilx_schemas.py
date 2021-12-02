#pylint: disable=E0611,W0105

from typing import List
from pydantic import BaseModel

"""
Validate SOURCE RESPONSE BODY SCHEMA
"""


class Items(BaseModel):
    dsku: int
    quantityShipped: int
    quantityOrdered: int


class Response(BaseModel):
    id: str
    release: str
    transactionType: str
    items: List[Items]
    poNumber: str


class Validator(BaseModel):
    response: List[Response]

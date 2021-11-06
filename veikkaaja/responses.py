"""Collection of the parsing functionality of different API responses"""
from datetime import datetime
from enum import Enum
from typing import NamedTuple

from veikkaaja import logger
from veikkaaja.types import GameTypes, ParseableEnum


class TransActionType(ParseableEnum):
    """A enumeration of all possible transaction types"""
    WIN = "WIN"
    LOSS = "LOSS"
    BUY = "BUY"

class Wager(NamedTuple):
    """The result of a query for transactions"""
    result: TransActionType
    amount: int
    accounting_date: datetime
    external_id: str
    id: int
    product: GameTypes

class ResponseType(Enum):
    """Enumeration of each possible response from the veikkaus api"""
    TRANSACTION_LIST = 0

def parse_date(unix_date: str):
    """The API responses contain unix timestamp, parse it"""
    return datetime.fromtimestamp(int(unix_date) / 1000)

def parse_response(response: dict, response_type: ResponseType):
    """A common parsing entry point for all parsing functionality"""

    if response_type == ResponseType.TRANSACTION_LIST:
        return parse_transaction_list(response)

    logger.warning("Response of type %s could not be parsed", response_type)
    return None

def parse_transaction_list(response: dict):
    """Parsing response to EndPoint.account_betting_history"""

    data = response['transactions']
    wagers = []
    for wager in data:
        wagers.append(Wager(
            external_id=wager['externalId'],
            id=wager['id'],
            accounting_date=parse_date(wager['accountingDate']),
            amount=wager['amount'],
            result=TransActionType.parse(wager['type']),
            product=GameTypes.parse(wager['product'])
        ))

    return wagers

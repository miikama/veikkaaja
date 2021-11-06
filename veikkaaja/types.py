"""Collection of types"""
from enum import Enum


class ParseableEnum(Enum):
    """A useful enumeration which provides a parse method"""

    @classmethod
    def parse(cls, string):
        """Parse which enumeration corresponse to the input string"""
        for value in cls:
            if value.value == string:
                return value

        raise ValueError(f"Input string {string} did not match any enumeration for class {cls}")

class GameTypes(ParseableEnum):
    """Available gamemodes in the API"""
    MULTISCORE = "MULTISCORE"  # Moniveto
    SCORE = "SCORE"  # Tulosveto
    SPORT = "SPORT"  # Vakio
    WINNER = "WINNER"  # Voittajavedot
    PICKTWO = "PICKTWO"  # Päivän pari
    PICKTHREE = "PICKTHREE"  # Päivän trio
    PERFECTA = "PERFECTA"  # Superkaksari
    TRIFECTA = "TRIFECTA"  # Supertripla
    EBET = "EBET"  # Pitkäveto
    RAVI = "RAVI"  # Moniveikkaus

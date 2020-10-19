"""A small script to invoke a client through all the supported
endpoints and save the sent out requests and responses.
"""
import json
from pathlib import Path
from typing import Any, Dict

import requests

from veikkaaja.endpoints import EndPoint
from veikkaaja.veikkaus_client import (BetDecision, BetTarget, GameTypes,
                                       VeikkausClient)


class SavingClient(VeikkausClient):
    """A small client that saves the outgoing and incoming
    API requests/responses under
    'api_requests/endpoint' and 'api_responsese/endpoint'
    """

    def save_outgoing_request(self, endpoint: EndPoint, payload: Dict[Any, Any]):
        """For testing, add and interface for saving the outgoing messages."""
        out_folder = Path(__file__).parent / "api_requests" / (
            endpoint.endpoint.replace('/', '.') + '.json')
        with out_folder.open('w') as file_handle:
            json.dump(payload, file_handle)

    def save_incoming_response(self, endpoint: EndPoint, response: requests.Response):
        """For testing, add and interface for saving the incoming responses."""
        out_folder = Path(__file__).parent / "api_responses" / (
            endpoint.endpoint.replace('/', '.') + ".json")
        with out_folder.open('w') as file_handle:
            json.dump(response.json(), file_handle)


def main():
    """A test function"""
    client = SavingClient()

    # get balances
    client.get_balance()

    # get upcoming EBET (Pitkäveto) draws
    games = client.upcoming_events(GameTypes.EBET)

    if not games:
        return

    # place bet on the first game
    game = games[-1]
    print("\n\nplacing bet for game:\n{}\n".format(game))

    success = client.place_bet(game, BetDecision(BetTarget.HOME, 100), test=True)
    assert success, "Could not place bet"

    # available sports
    client.sport_types()

    # available categories for football
    client.sport_categories(1)

    # tournaments for football and england
    client.sport_tournaments(1, 2)

    # info on the england main football league
    client.sport_tournament_info(1, 2, 1)


if __name__ == "__main__":
    main()
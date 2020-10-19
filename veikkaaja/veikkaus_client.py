"""Main veikkaus client module"""
import json
import os
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Union

import requests

from veikkaaja import logger
from veikkaaja.endpoints import EndPoint


class GameTypes(Enum):
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


class BetTarget(Enum):
    """Currently only 1x2 supported"""
    HOME = "HOME"
    X = "X"
    AWAY = "AWAY"


class BetDecision(NamedTuple):
    """Currently only 1x2 supported"""
    # what to be
    target: BetTarget
    # how much to bet in cents
    amount: int


class Game:
    """A class for holding EBET event information"""

    # pylint:disable=too-many-instance-attributes
    # This is intended just as a wrapper to hold the
    # data in the API response

    home_team = ""
    away_team = ""
    home_odds = 0.0
    away_odds = 0.0
    draw_odds = 0.0
    event_id = 0
    row_id = 0
    draw_type = ""  # 1x2
    status = ""
    brand_name = 0
    close_time = datetime.fromtimestamp(0)
    league = ""
    sport_id = 0

    def __init__(self, client: 'VeikkausClient'):
        """"""
        self._client: VeikkausClient = client

    def place_bet(self, bet: BetDecision):
        """Given amount in cents, bet for target."""
        self._client.place_bet(self, bet)

    def __repr__(self):
        """Make nicer output"""
        close_str = self.close_time.strftime("%d.%m.%Y %H:%M")
        return f"{self.__class__.__name__:} type: '{self.draw_type:3}' {close_str} {self.league}: {self.home_team:15} - {self.away_team:15} id: {self.row_id} event_id: {self.event_id} status: {self.status}, odds: ({self.home_odds:6} - {self.draw_odds:6} - {self.away_odds:6})"  #pylint:disable=line-too-long


class EventInfo:
    """A wrapper to keep information of the EBET draws"""
    league = ""
    external_id = ""

    def __repr__(self):
        return f"{self.__class__.__name__}: league: {self.league}, external_id: {self.external_id}"


class VeikkausClient:
    """The main client that holds on the API session"""

    API_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-ESA-API-Key": "ROBOT"
    }

    def __init__(self, account="", password=""):
        """
        Arguments:
            account (str):  Name of the account or empty if empty
                            account name is loaded from VEIKKAUS_ACCOUNT
                            environment variable.
            password (str): account password. If empty, loaded from
                            VEIKKAUS_PASSWORD environment variable
        """

        acc_password = password
        if not acc_password:
            if "VEIKKAUS_PASSWORD" not in os.environ:
                raise RuntimeError("Missing account authentication information")
            acc_password = os.environ['VEIKKAUS_PASSWORD']

        acc = account
        if not acc:
            if "VEIKKAUS_ACCOUNT" not in os.environ:
                raise RuntimeError("Missing account authentication information")
            acc = os.environ['VEIKKAUS_ACCOUNT']

        self.session = self.login(acc, acc_password)

    def _access_endpoint(self,
                         endpoint: EndPoint,
                         payload: Dict[str, Any] = None,
                         method="GET") -> Union[requests.Response, None]:
        """
        A common wrapper for sending and logging API requests

        Arguments:
            endpoint: the url of the endpoint
            payload: dictionary of the query parameters
            method: GET or POST
        """
        payload = {} if payload is None else payload

        if not self.session:
            logger.warning("No active session for accessing '%s'.", endpoint.endpoint)
            return None

        # log sending out a request
        payload_text = "\n{}".format(json.dumps(payload, indent=4)) if payload else ""
        logger.info("\033[93mSending\033[0m %s %s:%s", method, endpoint.url, payload_text)

        self.save_outgoing_request(endpoint, payload)

        if method == "GET":
            response = self.session.get(
                endpoint.url, headers=self.API_HEADERS, params=payload)
        elif method == "POST":
            response = self.session.post(
                endpoint.url, headers=self.API_HEADERS, json=payload)
        else:
            raise RuntimeError("Unsupported method {}".format(method))

        self.save_incoming_response(endpoint, response)

        if response.status_code != 200:
            # log out the error
            logger.warning("hello")
            logger.error("\033[91mRequest failed\033[0m %s, %s. URL: %s",
                         response.status_code, response.reason, response.url)

            # RED debug log entry
            if response.content:
                logger.debug("\033[91mInvalid request:\033[0m\n%s", response.content)
            return None

        # green dedub log entry, the responses are quite large
        logger.info("\033[92mResponse OK\033[0m from %s", endpoint.endpoint)
        logger.debug("\033[92mReceived:\033[0m\n%s",
                     json.dumps(response.json(), indent=4))

        return response

    def save_outgoing_request(self, endpoint: EndPoint, payload: Dict[Any, Any]):
        """For testing, add and interface for saving the outgoing messages."""

    def save_incoming_response(self, endpoint: EndPoint, response: requests.Response):
        """For testing, add and interface for saving the incoming responses."""

    def login(self, account: str, password: str):
        """
        Starts and returns a requests session.

        Returns:
            requests.Session or None if login failed.
        """
        login_payload = {"type": "STANDARD_LOGIN", "login": account, "password": password}
        logger.info("Trying to log in...")
        logger.info("\033[93mSending\033[0m %s %s", "GET",
                    EndPoint.login_endpoint().endpoint)
        session = requests.Session()
        response = session.post(
            EndPoint.login_endpoint(),
            data=json.dumps(login_payload),
            headers=self.API_HEADERS)

        if response.status_code != 200:
            logger.error("Cannot login")
            return None

        logger.info("\033[92mResponse OK\033[0m Succesfully logged in!")
        return session

    def get_balance(self, balance="usableBalance"):
        """Return the account balance
        Args:
            balance (str): the type of balance to return, options are
                           ('balance', 'usableBalance', 'frozenBalance')
        """
        assert balance in ('balance', 'usableBalance',
                           'frozenBalance'), "Invalid balance type"

        response = self._access_endpoint(EndPoint.account_info_endpoint(), method="GET")

        if response is None:
            return 0

        cash = response.json().get('balances', {}).get('CASH', {})
        logger.info("Account has balance: total: %s €, frozen: %s €, usable: %s €",
                    cash.get('balance', 0) / 100,
                    cash.get('frozenBalance', 0) / 100,
                    cash.get('usableBalance', 0) / 100)

        # return the requested balance
        return cash.get(balance, 0) / 100

    def upcoming_events(self, game_type: GameTypes) -> List[Game]:
        """Get upcoming games"""

        payload = {'game-names': game_type.value}
        response = self._access_endpoint(
            EndPoint.games_info_endpoint(), payload=payload, method="GET")

        if not response:
            return []

        data = response.json()

        if game_type == GameTypes.EBET:
            return self.parse_draws(data)

        logger.warning("Not yet implemented game type: %s", game_type.value)
        return []

    def parse_draws(self, data: Dict):
        """
        API response:

            "draws": [
            {
                "gameName": "EBET",
                "brandName": "838",
                "id": "2143963",
                "name": "SINGLE",
                "status": "OPEN",
                "openTime": 1600398000000,
                "closeTime": 1600887480000,
                "drawTime": 1600887600000,
                "resultsAvailableTime": 1600894799000,
                "gameRuleSet": {
                    "basePrice": 100,
                    "maxPrice": 1000000,
                    "stakeInterval": 10,
                    "minStake": 10,
                    "maxStake": 100000,
                    "minSystemLevel": 1,
                    "maxSystemLevel": 10,
                    "oddsType": "FIXED"
                },
                "rows": [
                    {
                        "id": "1",
                        "status": "OPEN",
                        "includedRowCount": 32,
                        "name": "",
                        "description": "",
                        "detailedDescription": "1/2",
                        "tvChannel": "",
                        "competitors": [
                            {
                                "id": "1",
                                "name": "Olympiakos",
                                "number": 133,
                                "odds": {
                                    "odds": 132
                                },
                                "status": "ACTIVE",
                                "handicap": "0.00"
                            },
                            {
                                "id": "2",
                                "name": "Omonoia",
                                "number": 313,
                                "odds": {
                                    "odds": 860
                                },
                                "status": "ACTIVE"
                            },
                            {
                                "id": "3",
                                "name": "Tasapeli",
                                "odds": {
                                    "odds": 440
                                },
                                "status": "ACTIVE"
                            }
                        ],
                        "eventId": "98723990",
                        "excludedEvents": [
                            "98723990"
                        ],
                        "type": "1X2",
                        "sportId": "1",
                        "externalId": "0"
                    }
                ]
            },

        """

        games = []
        for entry in data.get('draws', []):

            good = True
            game = Game(self)
            game.row_id = entry.get('id')
            game.brand_name = entry.get('brandName')
            game.status = entry.get('status')
            game.close_time = datetime.fromtimestamp(entry.get('closeTime', 0) / 1000)
            for row in entry.get('rows', []):

                game.event_id = row.get('eventId')
                game.status = row.get('status')
                game.draw_type = row.get('type')
                game.sport_id = row.get('sportId')
                for comp in row.get('competitors', []):
                    if comp.get('id') == "1":
                        game.home_team = comp.get('name')
                        game.home_odds = float(comp.get('odds').get('odds'))
                    if comp.get('id') == "2":
                        game.away_team = comp.get('name')
                        game.away_odds = float(comp.get('odds').get('odds'))
                    if comp.get('id') == "3":
                        if not comp.get('name') == "Tasapeli":
                            logger.debug("Skipping %s, since it has no 'Tasapeli' odds",
                                         row.get('name'))
                            good = False
                        game.draw_odds = float(comp.get('odds').get('odds'))

            if good:
                games.append(game)

        games = sorted(games, key=lambda game: game.close_time)
        return games

    def sport_types(self) -> List[Dict[str, str]]:
        """query available sport type ids:

        API Response:

        [
            {
                "id": "7",
                "name": "Salibandy"
            },
            {
                "id": "48",
                "name": "Arvontapelit"
            },
            {
                "id": "25",
                "name": "Kamppailulajit"
            }
        ]
        """
        payload = {'lang': "fi"}
        response = self._access_endpoint(
            EndPoint.sport_type_code_endpoint(), payload, method="GET")

        if not response:
            return []

        return response.json()

    def sport_categories(self, sport_id: int) -> List[Dict[str, str]]:
        """
        query available sport type subgateries

        e.g. for football query different countries
        that have football leagues.

        API Response:

        {
            "id": "1",
            "name": "Jalkapallo",
            "categories": [
                {
                    "id": "1",
                    "name": "Suomi"
                },
                {
                    "id": "2",
                    "name": "Englanti"
                },
                {
                    "id": "3",
                    "name": "Italia"
                },
        }
        """
        payload = {'lang': "fi"}
        response = self._access_endpoint(
            EndPoint.sport_categories_endpoint(sport_id), payload, method="GET")

        if not response:
            return []

        return response.json()

    def sport_tournaments(self, sport_id: int,
                          sport_category_id: int) -> List[Dict[str, str]]:
        """
        query available tournaments for sport type subgateries

        e.g. for football query different countries
        that have football leagues.

        API Response:
        {
            "id": "2",
            "name": "Englanti",
            "tournaments": [
                {
                    "id": "1",
                    "name": "Valioliiga"
                },
                {
                    "id": "2",
                    "name": "Mestaruussarja"
                },
                {
                    "id": "3",
                    "name": "Ykk\u00f6sliiga"
                },
            ]
        }
        """

        payload = {'lang': "fi"}
        response = self._access_endpoint(
            EndPoint.sport_tournaments_endpoint(sport_id, sport_category_id),
            payload,
            method="GET")

        if not response:
            return []

        return response.json()

    def sport_tournament_info(self, sport_id: int, sport_category_id: int,
                              sport_tournament_id) -> List[Dict[str, str]]:
        """
        query available tournaments for sport type subgateries

        e.g. for football query different countries
        that have football leagues.

        API Response:
        {
            "id": "1",
            "name": "Valioliiga",
            "events": [
                {
                    "id": "94772195",
                    "name": "Crystal P - Bournemouth",
                    "date": 1557669600000
                },
                ...
            ],
            "teams": [
                {
                    "id": "60",
                    "name": "Huddersfield",
                    "shortName": "Huddersfield"
                },
                {
                    "id": "446",
                    "name": "Hull",
                    "shortName": "Hull"
                },
                ...
            ],
        }

        """

        payload = {'lang': "fi"}
        response = self._access_endpoint(
            EndPoint.sport_tournament_info_endpoint(sport_id, sport_category_id,
                                                    sport_tournament_id),
            payload,
            method="GET")

        if not response:
            return []

        return response.json()

    def event_info(self, event_id: int) -> Union[EventInfo, None]:
        """Query more specific information for the event

        API response:
            {
                "id": "98587029",
                "name": "Liverpool - Arsenal",
                "sportId": "1",
                "sportName": "Jalkapallo",
                "categoryId": "2",
                "categoryName": "Englanti",
                "tournamentId": "1",
                "tournamentName": "Valioliiga",
                "teams": [
                    {
                        "id": "1",
                        "name": "Arsenal",
                        "shortName": "Arsenal"
                    },
                    {
                        "id": "9",
                        "name": "Liverpool",
                        "shortName": "Liverpool"
                    }
                ],
                "date": 1601319600000,
                "externalId": "23203829",
                "hasLiveBetting": false
            }

        """

        payload = {'lang': "fi"}
        response = self._access_endpoint(
            EndPoint.single_event_info_endpoint(event_id), payload, method="GET")

        if not response:
            return None

        data = response.json()

        event = EventInfo()
        event.league = data.get('tournamentName')
        event.external_id = data.get('externalId')

        return event

    def draw_info(self, draw_id: int) -> Union[EventInfo, None]:
        """Query more specific information for a single draw

        API response:
        {
            "id": "98587029",
            "name": "Liverpool - Arsenal",
            "sportId": "1",
            "sportName": "Jalkapallo",
            "categoryId": "2",
            "categoryName": "Englanti",
            "tournamentId": "1",
            "tournamentName": "Valioliiga",
            "teams": [
                {
                    "id": "1",
                    "name": "Arsenal",
                    "shortName": "Arsenal"
                },
                {
                    "id": "9",
                    "name": "Liverpool",
                    "shortName": "Liverpool"
                }
            ],
            "date": 1601319600000,
            "externalId": "23203829",
            "hasLiveBetting": false
        }
        """

        payload = {'lang': "fi"}

        response = self._access_endpoint(
            EndPoint.single_draw_info_endpoint(draw_id), payload, method="GET")

        if not response:
            return None

        data = response.json()

        event = EventInfo()
        event.league = data.get('tournamentName')
        event.external_id = data.get('externalId')

        return event

    def place_bet(self, game: Game, bet: BetDecision, test=True) -> bool:
        """Place a bet, bet amount in cents

        Arguments:
            game: which draw to place the bet for
            bet: what to bet
            test: (optional) whether to use the API test endpoint
                    which does not actually place the bet, just checks
                    that it could have been placed
        """
        endpoint = EndPoint.place_wager_endpoint()
        if test:
            endpoint = EndPoint.place_wager_test_endpoint()

        payload = self.ebet_payload([game], [bet])

        response = self._access_endpoint(endpoint, payload=payload, method="POST")

        if not response:
            return False

        return True

    @staticmethod
    def ebet_payload(games: List[Game], bets: List[BetDecision]):
        """
        Payload for ebet wager:
        https://github.com/VeikkausOy/sport-games-robot/blob/master/doc/ebet-single-wager-request.json

        API payload:
            [
                {
                    "gameName": "EBET",
                    "requestId": "request-19",
                    "selections": [
                        {
                            "betType": "SINGLE",
                            "competitors": {
                                "main": [
                                    "1"
                                ],
                                "spare": [
                                    "310"
                                ]
                            },
                            "rowId": "150410",
                            "stake": 100,
                            "systemBetType": "SYSTEM"
                        },
                        {
                            "betType": "SINGLE",
                            "competitors": {
                                "main": [
                                    "3"
                                ],
                                "spare": [
                                    "220"
                                ]
                            },
                            "rowId": "150411",
                            "stake": 100,
                            "systemBetType": "SYSTEM"
                        }
                    ],
                    "type": "NORMAL"
                }
            ]
        """
        assert len(games) == len(bets), "Number of games has to match number of bets"

        def selected_play(game: Game, target: BetTarget):
            if target == BetTarget.HOME:
                return "1", game.home_odds
            if target == BetTarget.X:
                return "2", game.draw_odds
            if target == BetTarget.AWAY:
                return "3", game.away_odds
            raise TypeError("invalid bet target {}".format(target.value))

        data = []
        for game, bet in zip(games, bets):
            game_data = {
                "type": "NORMAL",
                "gameName": GameTypes.EBET.value,
            }
            # Loading of the data could be refactored into a
            # cleaner typed dataclass, for now ignore types
            game_data["selections"] = [{    # type: ignore
                "systemBetType": "NORMAL",
                "stake": bet.amount,
                "competitors": {
                    "main": [selected_play(game, bet.target)[0]],
                    "spare": [int(selected_play(game, bet.target)[1])],
                },
                "rowId": game.row_id,
            }]
            data.append(game_data)

        return data


def print_sport_info(client: VeikkausClient):
    """Print example info available for football"""
    # available sports
    sport_ids = client.sport_types()
    print(json.dumps(sport_ids, indent=4))
    # available categories for football
    fb_categories = client.sport_categories(1)
    print(json.dumps(fb_categories, indent=4))

    fb_tournaments = client.sport_tournaments(1, 2)
    print(json.dumps(fb_tournaments, indent=4))

    fb_tournament = client.sport_tournament_info(1, 2, 1)
    print(json.dumps(fb_tournament, indent=4))


def main():
    """A test function"""
    client = VeikkausClient()

    # get balances
    client.get_balance()

    # get upcoming EBET (Pitkäveto) draws
    games = client.upcoming_events(GameTypes.EBET)
    logger.info(games[0])
    logger.info("and %s other games", len(games) - 2)
    logger.info(games[-1])

    if not games:
        return

    # place bet on the first game
    game = games[-1]
    print("\n\nplacing bet for game:\n{}\n".format(game))

    success = client.place_bet(game, BetDecision(BetTarget.HOME, 100), test=True)

    if success:
        logger.info("\033[32mSUCCESS\033[0m bet placed")

    # print_sport_info(client)


if __name__ == "__main__":
    main()

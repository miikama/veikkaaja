"""Keep the endpoints separate"""


from datetime import date


class EndPoint:
    """Container for the API endpoints"""

    API_ENDPOINT = "https://www.veikkaus.fi/api"

    def __init__(self, endpoint_suffix: str):
        """
        Arguments:
            endpoint_suffix: the part of the endpoint url
                that comes after the API_ENDPOINT
        """
        self.endpoint = endpoint_suffix
        self.url = f"{self.API_ENDPOINT}/{self.endpoint}"

    def __repr__(self):
        """Only show the endpoint"""
        return self.url

    @classmethod
    def login_endpoint(cls):
        """place for initializing session v1/sessions"""
        return cls("bff/v1/sessions")

    @classmethod
    def account_info_endpoint(cls):
        """query account information v1/players/self/account"""
        return cls("v1/players/self/account")

    @classmethod
    def account_betting_history(cls):
        """query account information v1/players/self/account
        https://github.com/VeikkausOy/sport-games-robot/issues/95
        """
        return cls("v1/players/self/account/transactions")

    @classmethod
    def wager_information(cls, event_id):
        """query account information
        The correct endpoint depends on the wager type,
        that would have to be tracked somewhere, but the queries
        to transactions do not return information about event type
        related to transactions. There are at least three
        different endpoints for wager information:

            - ebet-wager-details/v1/tickets/external-id
            - sport-wager-details/v1/tickets/external-id
            - draw-wager-details/v1/tickets/external-id

        See https://github.com/VeikkausOy/sport-games-robot/issues/16
        """
        return cls(f"ebet-wager-details/v1/tickets/{event_id}")

    @classmethod
    def games_info_endpoint(cls):
        """get info of upcoming games
        Used to be 'odj/v2/sport-games/draws' but it seems
        that the 'odj' was dropped at some point
        """
        return cls("sport-open-games/v1/games/EBET/draws")

    @classmethod
    def closed_games_by_day(cls, day: date):
        """The information for closed games can be found on a specific endpoint
        https://github.com/VeikkausOy/sport-games-robot/issues/142


        # a specific event:  return cls("ebet-results/v1/games/EBET/draws/2425549")
        # for specific date: return cls("ebet-results/v1/games/EBET/draws/by-day/2021-11-04")
        """
        formatted_date = day.strftime("%Y-%m-%d")
        return cls(f"ebet-results/v1/games/EBET/draws/by-day/{formatted_date}")

    @classmethod
    def single_event_info_endpoint(cls, event_id: int):
        """get info of upcoming games"""
        return cls(f"v1/sports/events/{event_id}")

    @classmethod
    def single_draw_info_endpoint(cls, draw_id: int):
        """get info of upcoming games"""
        return cls(f"odj/v2/sport-games/draws/{draw_id}")

    @classmethod
    def place_wager_test_endpoint(cls):
        """check if the placed bet is valid"""
        return cls("sport-interactive-wager/v1/tickets/check")
        # return cls("v1/sport-games/wagers/check")

    @classmethod
    def place_wager_endpoint(cls):
        """check if the placed bet is valid"""
        return cls("sport-interactive-wager/v1/tickets")
        # return cls("v1/sport-games/wagers")

    @classmethod
    def sport_type_code_endpoint(cls):
        """get available sport codes"""
        return cls("v1/sports")

    @classmethod
    def sport_categories_endpoint(cls, sport_id: int):
        """get available categories for a sport"""
        return cls(f"v1/sports/{sport_id}")

    @classmethod
    def sport_tournaments_endpoint(cls, sport_id: int, sport_category_id: int):
        """get available tournaments for sport and category"""
        return cls(f"v1/sports/{sport_id}/categories/{sport_category_id}")

    @classmethod
    def sport_tournament_info_endpoint(cls, sport_id: int, sport_category_id: int,
                                       tournament_id: int):
        """get info for a specific sport, category, and tournament."""
        return cls(
            f"v1/sports/{sport_id}/categories/{sport_category_id}/tournaments/{tournament_id}"
        )

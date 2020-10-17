"""Keep the endpoints separate"""


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
    def games_info_endpoint(cls):
        """get info of upcoming games"""
        return cls("odj/v2/sport-games/draws")

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
        return cls("v1/sport-games/wagers/check")

    @classmethod
    def place_wager_endpoint(cls):
        """check if the placed bet is valid"""
        return cls("v1/sport-games/wagers")

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
    def sport_tournament_info_endpoint(cls, sport_id: int,
                                       sport_category_id: int,
                                       tournament_id: int):
        """get info for a specific sport, category, and tournament."""
        return cls(
            f"v1/sports/{sport_id}/categories/{sport_category_id}/tournaments/{tournament_id}"
        )

"""Test whether the CI can access some basic API endpoints"""

from unittest import TestCase

from veikkaaja.veikkaus_client import GameTypes

from .mock_client import MockClient


class TestEbetBetting(TestCase):
    """test access to API"""

    def test_parsing_queried_ebet_events(self):
        """Set up an invalid gametype"""
        client = MockClient()
        games = client.upcoming_events(GameTypes.EBET)

        self.assertIsNotNone(games)
        self.assertEqual(len(games), 269)

        found_roda_telstar_game = False
        for game in games:
            self.assertIsNotNone(game)

            # info for a single specific game
            if game.home_team == "Roda JC" and game.away_team == "Telstar":
                found_roda_telstar_game = True
                self.assertEqual(game.draw_type, "1X2")
                self.assertEqual(game.event_id, "98744678")
                self.assertEqual(game.row_id, "2186938")
                self.assertEqual(game.status, "OPEN")
                self.assertEqual(game.home_odds, 188.0)
                self.assertEqual(game.draw_odds, 375.0)
                self.assertEqual(game.away_odds, 320.0)

        self.assertTrue(found_roda_telstar_game)

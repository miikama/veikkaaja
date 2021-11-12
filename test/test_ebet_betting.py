"""Test whether the CI can access some basic API endpoints"""

from unittest import TestCase

from veikkaaja.veikkaus_client import EBETType, GameTypes

from .mock_client import MockClient


class TestEbetBetting(TestCase):
    """test access to API"""

    def test_parsing_queried_ebet_events(self):
        """Set up an invalid gametype"""
        client = MockClient()
        games = client.upcoming_events(GameTypes.EBET)

        games = list(filter(lambda game: game.draw_type == EBETType.ONE_X_TWO, games))

        self.assertIsNotNone(games)
        self.assertEqual(len(games), 239)

        found_edinburgh_stanraer_game = False
        for game in games:
            self.assertIsNotNone(game)

            # info for a single specific game
            if game.home_team == "Edinburgh C" and game.away_team == "Stranraer":
                found_edinburgh_stanraer_game = True
                self.assertEqual(game.draw_type, EBETType.ONE_X_TWO)
                self.assertEqual(game.event_id, "101152897")
                self.assertEqual(game.row_id, 2799985)
                self.assertEqual(game.list_index, "6752")
                self.assertEqual(game.status, "OPEN")
                self.assertEqual(game.home_odds, 245.0)
                self.assertEqual(game.draw_odds, 330.0)
                self.assertEqual(game.away_odds, 250.0)

        self.assertTrue(found_edinburgh_stanraer_game)

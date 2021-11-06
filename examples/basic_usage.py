"""Basic usage example"""

import json

from veikkaaja import logger
from veikkaaja.veikkaus_client import (BetDecision, BetTarget, GameTypes,
                                       VeikkausClient)


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

    events = client.get_betting_history()

    for event in events:
        print(event)
        client.get_bet_event_information(event)

    # get upcoming EBET (Pitkäveto) draws
    games = client.upcoming_events(GameTypes.EBET)
    logger.info(games[0])
    logger.info("and %s other games", len(games) - 2)
    logger.info(games[-1])

    if not games:
        return

    # place bet on the first game
    game = games[-1]
    print(f"\n\nplacing bet for game:\n{game}\n")

    success = client.place_bet(game, BetDecision(BetTarget.HOME, 100), test=True)

    if success:
        logger.info("\033[32mSUCCESS\033[0m bet placed")

    # print_sport_info(client)


if __name__ == "__main__":
    main()
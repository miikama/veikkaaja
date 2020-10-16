
# Veikkaaja

Veikkaaja is a straight-forward wrapper for the `Veikkaus` betting API. This package is not affiliated with Veikkaus in any way, use at your own peril. An official description of the API and the entrypoints can be found at [Veikkaus reference implementation](https://github.com/VeikkausOy/sport-games-robot)

The Veikkaus API is quite extensive, endpoints for getting the game information and enabling betting are supported for the following game modes: 

|  |  |
|-----------|----------|
|MULTISCORE | Moniveto |
|SCORE | Tulosveto |
|SPORT | Vakio |
|WINNER | Voittajavedot|
|PICKTWO | Päivän pari|
|PICKTHREE | Päivän trio|
|PERFECTA | Superkaksari|
|TRIFECTA | Supertripla|
|EBET | Pitkäveto|
|RAVI | Moniveikkaus|


Currently, only endpoints for EBET (Pitkäveto) are implemented in this wrapper. Contributions for the rest of the endpoints are welcome.


## Installation 

This package is available at [PyPI](pypi.org). Install with `pip`:

```bash
pip install veikkaaja
```

## Usage

For accessing the API endpoints, you need a valid Veikkaus-account. You can provide the account information as arguments to the `VeikkausClient` upon initialization or as environment variables. If not provided as arguments to the client, the account information is read from the following environment variables:

```sh
export VEIKKAUS_ACCOUNT=user.name
export VEIKKAUS_PASSWORD=my-password
```

Betting is quite straight-forward

```python
from veikkaaja import VeikkausClient

client = VeikkausClient('user.name', 'my-password')
```

Getting you account balance

```python
client.get_balance())
0.0
```

Get the available games:

```python
# get upcoming EBET (Pitkäveto) draws
games = client.upcoming_events(GameTypes.EBET)
print(games[0])
Game type: '12 ' 25.10.2020 02:58 : Khabib          - J.Gaethje       id: 2170768 event_id: 98816225 status: OPEN, odds: ( 131.0 - 0 -  320.0)
```

Select a game and bet:

```python
# place bet on the selected game
game = games[0]
success = client.place_bet(game,
                            BetDecision(BetTarget.HOME, 100),   # The amount to bet is given in cents
                            test=True)
```

Veikkaus API also provides a testing endpoint, which can be used to validate your bets before actually submitting them. If you set the `test=True` argument in the betting function call, the testing endpoint is used instead. 

> Note: The testing endpoint is the default, set test=False to actually place bets.

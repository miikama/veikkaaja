# Testing veikkaaja

The overall testing strategy is to avoid queries to the actual Veikkaus API endpoints when running tests. Mainly because it would create too much hassle with the Veikkaus credentials.

For tests that make actual queries to the Veikkaus endpoints, one should set the tests to be skipped if they are executed in the Github CI context, where credentials are not made available.

```python
# test_access.py
@unittest.skipIf('CI' in os.environ, "This is not currently run in Github CI.")
def test_login(self):
    """Login is attempted upon client initialization"""

    client = VeikkausClient()
    self.assertIsNotNone(client.session)
```

To be able to test the main functionality of the `veikkaaja` package, namely parsing the data from the Veikkaus API and sending correct data to the API, we mock the API responses with `responses` package. To updated or add new tests, one should:

1. login to Veikkaus API with their own credentials
2. Add queries to the new endpoints to `save_api_requests_responses.py`
3. Run `save_api_requests_responses.py`

which sends the queries to the API endpoints and saves the sent requests and obtained responses under `test/api_requests` and `test/api_responses`, respectively. The tests should then initiate an instance of `MockClient` instead of the actual `VeikkausClient` to obtain responses from the saved queries.

```python
# test_ebet_betting.py
from .mock_client import MockClient

class TestEbetBetting(TestCase):
    """test access to API"""

    def test_parsing_queried_ebet_events(self):
        """Set up an invalid gametype"""
        client = MockClient()
        games = client.upcoming_events(GameTypes.EBET)
```

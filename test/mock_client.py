"""A client for testing.

This mock client does not actually send any requests
over the network, but rather uses responses stored from
previous valid queries to the API
"""
import json
from pathlib import Path
from typing import Any, Dict, Union

import requests
import responses

from veikkaaja.endpoints import EndPoint
from veikkaaja.veikkaus_client import VeikkausClient


class MockClient(VeikkausClient):
    """Do not try to actually login"""

    def __init__(self):  # pylint: disable=super-init-not-called
        """Replace the original initialization
        that requires account information is given as
        arguments os as environment variables

        Do not try to login to the API

        Register all saved api responses as 'responses' as
        available endpoints.
        """

        saved_responses = (Path(__file__).parent / 'api_responses').glob('*.json')

        # For each saved actual json response from the real API
        # register a callback with responses that would return
        # the same json content that the real query would have returned.
        for response in saved_responses:
            # TODO: We just assume that we do not POST
            # and GET same endpoints.
            responses.add(
                responses.POST,
                EndPoint.API_ENDPOINT + "/" + response.stem.replace('.', '/'),
                match_querystring=False,
                json=json.loads(response.read_text()))
            responses.add(
                responses.GET,
                EndPoint.API_ENDPOINT + "/" + response.stem.replace('.', '/'),
                match_querystring=False,
                json=json.loads(response.read_text()))

    @responses.activate
    def _access_endpoint(self,
                         endpoint: EndPoint,
                         payload: Dict[str, Any] = None,
                         method="GET"):
        """
        Override the common entrypoint that sends out requests

        Check if we have stored a correct response from the API for this
        request and return that instead of trying to actually query
        a response from the API.
        """

        # check if we have the corresponding request/response files available
        request_file = Path(__file__).parent / 'api_requests' / endpoint.endpoint.replace(
            '/', '.')
        if request_file.exists():
            print("Found target request for {}".format(endpoint.endpoint))
            print(request_file.read_text())
        # TODO: Found a saved request, compare this request to it

        # we have registered the response with 'responses'
        # Now we just go and get it
        if method == "GET":
            response = requests.get(
                endpoint.url, headers=self.API_HEADERS, params=payload)
        elif method == "POST":
            response = requests.post(endpoint.url, headers=self.API_HEADERS, json=payload)
        else:
            raise RuntimeError("Unsupported method {}".format(method))

        if response.status_code != 200:
            return None
        return response

"""REST client handling, including aftershipStream base class."""

from __future__ import annotations
from datetime import datetime, timedelta
import sys
from typing import Any, Callable, Iterable

import requests, logging
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BasePageNumberPaginator
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


logger = logging.getLogger(__name__)

class TrackingsPaginator(BasePageNumberPaginator):
    """Paginator for the trackings AfterShip stream."""

    def has_more(self, response: requests.Response) -> bool:
        response_json = response.json()
        if (
            "data" in response_json
            and "trackings" in response_json["data"]
            and response_json["data"]["trackings"]
        ):
            return True
        else:
            return False


class aftershipStream(RESTStream):
    """aftership stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""

        return f"https://api.aftership.com/tracking/{self.config.get('api_version')}"

    records_jsonpath = "$.data.trackings[*]"  
    next_page_token_jsonpath = "$.data.page"  # noqa: S105

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="as-api-key",
            value=self.config.get("api_key", ""),
            location="header",
        )

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Get a new TrackingsPaginator for the trackings API endpoint."""
        return TrackingsPaginator(start_value=1)

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        params["limit"] = 200
        params["updated_at_max"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 

        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            replication_key_value = self.get_starting_replication_key_value(context)

            params["updated_at_min"] = datetime.strptime(replication_key_value, "%Y-%m-%dT%H:%M:%S%z") + timedelta(0,1)
            
        else:
            params["updated_at_min"] = self.config.get("start_date")

        return params


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())


    def backoff_max_tries(self) -> int:
        """The number of attempts before giving up when retrying requests.

        Returns:
            Number of max retries.
        """
        return 15

    def validate_response(self, response: requests.Response) -> None:
        """
        API responses require custom error handling as the error codes are hidden under 200 return codes.
        """
        if response.status_code == 429:
            retry_after = 2
            msg = (
                f"{response.status_code} Server Error: "
                f"{response.reason} for path: {self.path}. "
                f"Rate Limited: Waiting for 'Retry-after' value of {retry_after}."
            )
            time.sleep(retry_after)
            raise RetriableAPIError(msg)
        elif 400 <= response.status_code < 500:
            msg = (
                f"{response.status_code} Client Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise FatalAPIError(msg)
        elif 500 <= response.status_code < 600:
            msg = (
                f"{response.status_code} Server Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise RetriableAPIError(msg)

"""aftership tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th 

from tap_aftership import streams


class Tapaftership(Tap):
    """aftership tap class."""

    name = "tap-aftership"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True, 
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_version",
            th.StringType,
            default="2024-01",
            description="The url for the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.aftershipStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.TrackingsStream(self),
        ]


if __name__ == "__main__":
    Tapaftership.cli()

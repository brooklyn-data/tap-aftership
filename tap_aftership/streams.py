"""Stream type classes for tap-aftership."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th 

from tap_aftership.client import aftershipStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


class TrackingsStream(aftershipStream):
    """Define custom stream."""

    name = "trackings"
    path = "/trackings"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("last_updated_at", th.DateTimeType),
        th.Property("tracking_number", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("android", th.ArrayType(th.StringType)),
        th.Property("custom_fields", th.ObjectType(
            th.Property("item_names", th.StringType),
        )),
        th.Property("customer_name", th.StringType),
        th.Property("destination_country_iso3", th.StringType),
        th.Property("courier_destination_country_iso3", th.StringType),
        th.Property("emails", th.ArrayType(th.StringType)),
        th.Property("expected_delivery", th.StringType),
        th.Property("ios", th.ArrayType(th.StringType)),
        th.Property("note", th.StringType),
        th.Property("order_id", th.StringType),
        th.Property("order_id_path", th.StringType),
        th.Property("order_date", th.StringType),
        th.Property("origin_country_iso3", th.StringType),
        th.Property("shipment_package_count", th.IntegerType),
        th.Property("shipment_pickup_date", th.DateTimeType),
        th.Property("shipment_delivery_date", th.DateTimeType),
        th.Property("shipment_type", th.StringType),
        th.Property("shipment_weight", th.NumberType),
        th.Property("shipment_weight_unit", th.StringType),
        th.Property("signed_by", th.StringType),
        th.Property("smses", th.ArrayType(th.StringType)),
        th.Property("source", th.StringType),
        th.Property("tag", th.StringType),
        th.Property("subtag", th.StringType),
        th.Property("subtag_message", th.StringType),
        th.Property("title", th.StringType),
        th.Property("tracked_count", th.IntegerType),
        th.Property("last_mile_tracking_supported", th.BooleanType),
        th.Property("language", th.StringType),
        th.Property("unique_token", th.StringType),
        th.Property("checkpoints", th.ArrayType(th.ObjectType(
            th.Property("checkpoint_time", th.DateTimeType),
            th.Property("city", th.StringType),
            th.Property("coordinates", th.ArrayType(th.StringType)),
            th.Property("country_iso3", th.StringType),
            th.Property("country_name", th.StringType),
            th.Property("created_at", th.DateTimeType),
            th.Property("events", th.ArrayType(th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("reason", th.AnyType),
            ))),
            th.Property("location", th.StringType),
            th.Property("message", th.StringType),
            th.Property("raw_tag", th.StringType),
            th.Property("slug", th.StringType),
            th.Property("state", th.StringType),
            th.Property("subtag", th.StringType),
            th.Property("subtag_message", th.StringType),
            th.Property("tag", th.StringType),
            th.Property("zip", th.StringType),
        ))),
        th.Property("subscribed_smses", th.ArrayType(th.StringType)),
        th.Property("subscribed_emails", th.ArrayType(th.StringType)),
        th.Property("return_to_sender", th.BooleanType),
        th.Property("order_promised_delivery_date", th.DateTimeType),
        th.Property("delivery_type", th.StringType),
        th.Property("pickup_location", th.StringType),
        th.Property("pickup_note", th.StringType),
        th.Property("courier_tracking_link", th.StringType),
        th.Property("first_attempted_at", th.DateTimeType),
        th.Property("courier_redirect_link", th.StringType),
        th.Property("order_tags", th.ArrayType(th.StringType)),
        th.Property("order_number", th.StringType),
        th.Property("aftership_estimated_delivery_date", th.DateTimeType),
        th.Property("destination_raw_location", th.StringType),
        th.Property("latest_estimated_delivery", th.ObjectType(
                th.Property("date", th.StringType),
                th.Property("datetime_max", th.DateTimeType),
                th.Property("datetime_min", th.DateTimeType),
                th.Property("source", th.StringType),
                th.Property("specific", th.StringType)
        )),
        th.Property("courier_connection_id", th.AnyType),
        th.Property("latest_estimated_delivery", th.ObjectType(
                th.Property("date", th.StringType),
                th.Property("datetime_max", th.DateTimeType),
                th.Property("datetime_min", th.DateTimeType),
                th.Property("source", th.StringType),
                th.Property("specific", th.StringType)
        )),        
        th.Property("custom_estimated_delivery_date", th.DateTimeType),
        th.Property("origin_state", th.StringType),
        th.Property("origin_city", th.StringType),
        th.Property("origin_postal_code", th.StringType),
        th.Property("origin_raw_location", th.StringType),
        th.Property("destination_state", th.StringType),
        th.Property("destination_city", th.StringType),
        th.Property("destination_postal_code", th.StringType),
        th.Property("shipment_tags", th.ArrayType(th.StringType)),
        th.Property("next_couriers", th.ArrayType(th.ObjectType(
            th.Property("slug", th.StringType),
            th.Property("source", th.StringType),
            th.Property("tracking_number", th.StringType)
        ))),
        th.Property("transit_time", th.AnyType),
        th.Property("carbon_emissions", th.AnyType),
        th.Property("shipping_method", th.StringType),
        th.Property("location_id", th.StringType),
        th.Property("on_time_status", th.StringType),
        th.Property("on_time_difference", th.StringType),
        th.Property("tracking_account_number", th.StringType),
        th.Property("tracking_origin_country", th.StringType),
        th.Property("tracking_destination_country", th.StringType),
        th.Property("tracking_key", th.StringType),
        th.Property("tracking_postal_code", th.StringType),
        th.Property("tracking_ship_date", th.StringType),
        th.Property("tracking_state", th.StringType)
    ).to_dict()

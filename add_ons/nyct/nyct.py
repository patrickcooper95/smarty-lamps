from datetime import datetime
import json
import os
import time

import urllib.request
from google.transit import gtfs_realtime_pb2
import pandas as pd
import numpy as np

import utils
from utils import Config


# Get start time for recording when data was retrieved
ts = time.time()
start_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class Train:
    """
        This class provides the framework for a train object, created through the live transit data.
        For each unique train in the live transit feed, an object will be created detailing its service,
        stops, and stop times.

        While a class object does assign directions to trains (Uptown/Downtown) using the "assign_train" function,
        it mainly acts as a container for the train stops and times.
    """

    train_status_mapping = {
        0: "INCOMING_AT",
        1: "STOPPED_AT",
        2: "IN_TRANSIT_TO"
    }

    def __init__(self, feed_entity):
        ######## EXAMPLE DATA ########
        # trip_id: "136150_6..S01R"
        # start_date: "20221103"
        # route_id: "6"
        # current_stop_sequence: 37
        # current_status: STOPPED_AT
        # timestamp: 1667533101
        # stop_id: "639S"
        self._mask_schema(feed_entity)
        self.id = feed_entity.vehicle.trip.trip_id
        self.service = feed_entity.vehicle.trip.route_id
        self.start_date = feed_entity.vehicle.trip.start_date
        self.timestamp = feed_entity.vehicle.timestamp
        self.stop_id = feed_entity.vehicle.stop_id
        self.direction = self.orient_train()

    def orient_train(self):

        if self.stop_id:
            if "N" in self.stop_id:
                train_dir = "Uptown"
            else:
                train_dir = "Downtown"

            return train_dir

    def _mask_schema(self, entity):
        """Add values when they are not provided in the entity."""

        self.current_stop_sequence = entity.vehicle.current_stop_sequence \
            if hasattr(entity.vehicle, "current_stop_sequence") else None
        # statuses are stored in the Vehicle object as 0, 1 and 2 - mapped as part of Train class
        self.current_status = Train.train_status_mapping[entity.vehicle.current_status]


def _create_trains(feed, service: str):
    """
        The crucial function for the NYCT Project - this function parses the data from the transit feed,
        calls "create_train_lists" to create lists of this data; calls "create_dataframe" to align this data
        in a Pandas dataframe; and finally calls sort_dataframe to sort and add calculated fields to the DF.
    :return: a list of Train objects
    """
    trains = []
    for entity in feed.entity:
        if entity.HasField("vehicle") and entity.vehicle.trip.route_id == service:
            new_train = Train(entity)
            trains.append(new_train)
    return trains


def filter_stations(route_id, borough):
    """Filter the Stations manifest for only relevant stations."""
    stations_df = pd.read_csv("stations.csv")
    stations_df = stations_df[
        (stations_df["Borough"] == borough) &
        (stations_df["Daytime Routes"].str.contains(route_id))
    ]
    return stations_df


def get_trains(service: str, segment: str, create_json: bool = True, debug: bool = False):
    feed = gtfs_realtime_pb2.FeedMessage()
    header = gtfs_realtime_pb2.FeedHeader()
    en = gtfs_realtime_pb2.FeedEntity()

    # Get the feed endpoint for the specified service
    line_feed = Config[utils.get_nyct_feed(service)]
    req = urllib.request.Request(
        os.path.join(Config['base_gtfs_url'],
                     line_feed))

    with open("api_key", "r") as key_file:
        api_key = key_file.read()
    req.add_header("x-api-key", api_key)
    response = urllib.request.urlopen(req)
    response = response.read()
    feed.ParseFromString(response)

    stations_in_scope = filter_stations(service, segment)
    train_list = _create_trains(feed, service)

    if debug:
        for train in train_list:
            if train.stop_id[:-1] in stations_in_scope["GTFS Stop ID"].values:
                print(f"Trip ID: {train.id}\n"
                      f"Route ID: {train.service}\n"
                      f"Direction: {train.direction}\n"
                      f"Stop ID: {train.stop_id}\n"
                      f"Station: {stations_in_scope.loc[stations_in_scope['GTFS Stop ID'] == train.stop_id[:-1], 'Stop Name'].values[0]}\n"
                      f"Status: {train.current_status}\n"
                      f"Stop Sequence: {train.current_stop_sequence}\n")

    if create_json:
        output_list = []
        trains_in_scope = 0
        for train in train_list:
            if train.stop_id[:-1] in stations_in_scope["GTFS Stop ID"].values:
                trains_in_scope += 1
                output_list.append(
                    {
                        "trip_id": train.id,
                        "route_id": train.service,
                        "direction": train.direction,
                        "stop_id": train.stop_id,
                        "station": stations_in_scope.loc[
                            stations_in_scope['GTFS Stop ID'] == train.stop_id[:-1], 'Stop Name'
                        ].values[0],
                        "status": train.current_status,
                        "stop_sequence": train.current_stop_sequence
                    }
                )
        return {
            "timestamp": start_time,
            "subway_api_version": "0.0.1a",
            "total_train_count": len(train_list),
            "scoped_train_count": trains_in_scope,
            "station_count": len(stations_in_scope["GTFS Stop ID"].values),
            "data": output_list
        }


if __name__ == "__main__":
    result = get_trains("6", "M")
    with open("test_output.json", "w") as json_file:
        json.dump(result, json_file)

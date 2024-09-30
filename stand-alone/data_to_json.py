"""
This module is responsible for creating a formatted json file from
the generated raw data
"""
from configparser import ConfigParser
import json
from datetime import datetime, timedelta

parser = ConfigParser()
parser.read('data_to_json.ini')

version = parser.get('main', 'version')
labels = json.loads(parser.get('main', 'labels'))

start_date = datetime.strptime(parser.get('payload', 'start_date'), '%Y-%m-%dT%H:%M:%SZ')

time_increment = int(parser.get('payload', 'time_increment'))


loc_lon = ""
if parser.has_option('payload', 'loc_lon'):
    loc_lon = parser.get('payload', 'loc_lon')

loc_lat = ""
if parser.has_option('payload', 'loc_lat'):
    loc_lat = parser.get('payload', 'loc_lat')

meas_type = parser.get('payload', 'type')

unit = ""
if parser.has_option('payload', 'unit'):
    unit = parser.get('payload', 'unit')

time_change = timedelta(minutes=time_increment)

input_files = json.loads(parser.get('files', 'input_files'))
output_location = parser.get('files', 'output_dir')

for input_file in input_files:

    split_path = input_file.split("/")
    file_name = split_path[-1]
    split_file_name = file_name.split(".")
    device = split_file_name[0]

    payload = []

    time_runner = 0
    with open(input_file, 'r') as f:
        for line in f:
            new_measurement = {}

            new_measurement["type"] = meas_type

            new_measurement["when_captured"] = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            start_date = start_date + time_change

            new_measurement["device"] = device

            new_measurement["reading"] = float(line.rstrip())

            if loc_lat != "":
                new_measurement["loc_lat"] = float(loc_lat)

            if loc_lon != "":
                new_measurement["loc_lon"] = float(loc_lon)


            if unit != "":
                new_measurement["unit"] = str(unit)

            payload.append(new_measurement)


    new_json = {}
    new_json["version"] = int(version)
    new_json["labels"] = labels
    new_json["payload"] = payload

    output = output_location + '/' + device + '-' + meas_type + '.json'

    with open(output, 'w') as jf:
        json.dump(new_json, jf, indent=4)

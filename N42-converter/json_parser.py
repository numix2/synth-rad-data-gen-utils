import json

def parse_json(fileName: str) -> dict:
    """Reads in the omosjer json file, parses it and returns 
    a dictionary of lists with all the data in the json file
    """
    with open(fileName) as inf:
        input = json.load(inf)

    version = input["version"]
    payload = input["payload"]

    when_captured = []
    device = []
    loc_lat = []
    loc_lon = []
    mes_type = []
    reading = []
    real_time_dur = []
    live_time_dur = []
    energy_bin = []
    unit = []

    for measurment in payload:
        for key in measurment:
            if key == "when_captured":
                when_captured.append(measurment[key])
            if key == "device":
                device.append(measurment[key])
            if key == "loc_lat":
                loc_lat.append(measurment[key])
            if key == "loc_lon":
                loc_lon.append(measurment[key])
            if key == "type":
                mes_type.append(measurment[key])
            if key == "reading":
                reading.append(measurment[key])
            if key == "real_time":
                real_time_dur.append(measurment[key])
            if key == "live_time":
                live_time_dur.append(measurment[key])
            if key == "energy_bin":
                energy_bin.append(measurment[key])
            if key == "unit":
                unit.append(measurment[key])
        if "loc_lat" not in measurment:
            loc_lat.append(None)
        if "loc_lon" not in measurment:
            loc_lon.append(None)
        if "real_time" not in measurment:
            real_time_dur.append(None)
        if "live_time" not in measurment:
            live_time_dur.append(None)
        if "energy_bin" not in measurment:
            energy_bin.append(None)
        if "unit" not in measurment:
            unit.append(None)

    return  {
                "when_captured": when_captured,
                "device": device,
                "loc_lat": loc_lat,
                "loc_lon": loc_lon,
                "type": mes_type,
                "reading": reading,
                "real_time": real_time_dur,
                "live_time": live_time_dur,
                "energy_bin": energy_bin,
                "unit": unit
            }

#print(parse_json("example-4.json"))

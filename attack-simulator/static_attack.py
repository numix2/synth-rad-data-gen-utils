from datetime import datetime, timedelta
import tarfile
import pickle

from sklearn.preprocessing import MinMaxScaler
from ydata_synthetic.synthesizers.timeseries import TimeGAN

# ---------------------------------
# Public Methods
# ---------------------------------

def insert_one_event(file: dict,
                     frequency, # seconds
                     alarm_meas, # float value 
                     attack_lenght, # integer: how many measurement should be inserted after attack_start
                     attack_start # integer between 0 and the number of measurements inside one file
                     ) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)

    # build attack measurmenet
    attack_measurement = json_to_attack["payload"][attack_start].copy()
    attack_measurement["reading"] = float("{:.2f}".format(alarm_meas))

    seconds = timedelta(seconds=frequency)

    start_time = datetime.strptime(json_to_attack["payload"][attack_start]["when_captured"], '%Y-%m-%dT%H:%M:%SZ')
    next_time = start_time + seconds
    
    for i in range(attack_lenght):
        attack_measurement["when_captured"] = next_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        json_to_attack["payload"].insert((attack_start + i + 1), attack_measurement.copy())
        next_time = next_time + seconds
    
    return json_to_attack

## -----------------------------------------------------------------

def modify_x_to_event(file: dict, alarm_meas, attack_start, attack_lenght) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)
    
    for i in range(attack_lenght):
        if (attack_start + i) < len(json_to_attack["payload"]):
            json_to_attack["payload"][attack_start + i]["reading"] = alarm_meas

    return json_to_attack

# -----------------------------------------------------------------

def modify_x_to_zero(file: dict, attack_start, attack_lenght) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)
    
    for i in range(attack_lenght):
        if (attack_start + i) < len(json_to_attack["payload"]):
            json_to_attack["payload"][attack_start + i]["reading"] = 0.0
    
    return json_to_attack

#--------------------------------------------------------------

def modify_x_to_mean(file: dict, attack_start, attack_lenght) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)

    accum = 0.0
    for i in range(0, attack_start):
        accum += json_to_attack["payload"][i]["reading"]

    mean = accum / attack_start
    
    for i in range(attack_lenght):
        if (attack_start + i) < len(json_to_attack["payload"]):
            json_to_attack["payload"][attack_start + i]["reading"] = mean
    
    return json_to_attack

## -----------------------------------------------------------------

def modify_with_own_pattern(file: dict, attack_start, attack_lenght, pattern) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)

    attack_pattern = [pattern[i % len(pattern)] for i in range(attack_lenght)]
    
    for i, ap in enumerate(attack_pattern):
        if (attack_start + i) < len(json_to_attack["payload"]):
            json_to_attack["payload"][attack_start + i]["reading"] = ap

    return json_to_attack

## -------------------------------------------------------------------

def modify_with_past_pattern(file: dict, attack_start, attack_lenght) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)

    past_pattern = [m["reading"] for i, m in enumerate(json_to_attack["payload"]) if i < attack_start]
    attack_pattern = [past_pattern[i % len(past_pattern)] for i in range(attack_lenght)]
    
    for i, ap in enumerate(attack_pattern):
        if (attack_start + i) < len(json_to_attack["payload"]):
            json_to_attack["payload"][attack_start + i]["reading"] = ap

    return json_to_attack

## --------------------------------------------------------------------

def modify_to_generated(file: dict, attack_start, attack_lenght, model_tar_path) -> dict:
    json_to_attack = file.copy()
    json_to_attack = _add_attacked_label(json_to_attack)

    generated_data = _generate_synthetic_data(model_tar_path)
    unpacked_data = [data for packed_data in generated_data for data in packed_data]
    attack_data = [float("{:.2f}".format(unpacked_data[i])) for i in range(attack_lenght)]

    for i, gm in enumerate(attack_data):
        if (attack_start + i) < len(json_to_attack["payload"]):
            json_to_attack["payload"][attack_start + i]["reading"] = gm

    return json_to_attack

# -------------------------------------------
# Private Methods
# ------------------------------------------- 

def _add_attacked_label(file: dict) -> dict:
    file["labels"].append("attacked")
    return file


def _generate_synthetic_data(model_tar_path) -> list:
    archive = tarfile.open(model_tar_path)
    try:
        model_pickle = archive.extractfile('model.pkl')
        if model_pickle is not None:
            synth = TimeGAN.load(model_pickle)

            scaler_pickle = archive.extractfile('scaler.pkl')
            if scaler_pickle is not None:
                scaler = pickle.load(scaler_pickle)

                synth_data = synth.sample(1)

                synth_data = scaler.inverse_transform(synth_data[0])
    finally:
        archive.close()

    return synth_data.tolist()
"""
This is the main executable of the attack simulator. You can define attacks in the main section.
"""
import json
import os
from random import uniform, randint

from static_attack import *
from attack_enum import Attack


def perform_attack(input_dir: str, output_dir: str, attack: Attack, parameters: dict):
    json_file_names = [filename for filename in os.listdir(input_dir) if filename.endswith('.json')]

    for json_file_name in json_file_names:
        with open(os.path.join(input_dir, json_file_name)) as json_file:
            json_file = json.load(json_file)
        attacked_json = {}
        if attack is Attack.INSERT_ONE_EVENT:
            attacked_json = insert_one_event(
                json_file,
                randint(parameters["frequency"][0], parameters["frequency"][1]),
                uniform(parameters["alarm_meas"][0], parameters["alarm_meas"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1]),
                randint(parameters["attack_start"][0], parameters["attack_start"][1])
                )
        elif attack is Attack.MODIFY_X_TO_EVENT:
            attacked_json = modify_x_to_event(
                json_file,
                uniform(parameters["alarm_meas"][0], parameters["alarm_meas"][1]),
                randint(parameters["attack_start"][0], parameters["attack_start"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1])
                )
        elif attack is Attack.MODIFY_X_TO_ZERO:
            attacked_json = modify_x_to_zero(
                json_file,
                randint(parameters["attack_start"][0], parameters["attack_start"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1])
                )
        elif attack is Attack.MODIFY_X_TO_MEAN:
            attacked_json = modify_x_to_mean(
                json_file,
                randint(parameters["attack_start"][0], parameters["attack_start"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1])
                )
        elif attack is Attack.MODIFY_WITH_OWN_PATTERN:
            attacked_json = modify_with_own_pattern(
                json_file,
                randint(parameters["attack_start"][0], parameters["attack_start"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1]),
                parameters["pattern"]
                )
        elif attack is Attack.MODIFY_WITH_PAST_PATTERN:
            attacked_json = modify_with_past_pattern(
                json_file,
                randint(parameters["attack_start"][0], parameters["attack_start"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1]),
                )
        elif attack is Attack.MODIFY_WITH_GENERATED:
            attacked_json = modify_to_generated(
                json_file,
                randint(parameters["attack_start"][0], parameters["attack_start"][1]),
                randint(parameters["attack_lenght"][0], parameters["attack_lenght"][1]),
                parameters["model_tar_path"]
                )
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f"{output_dir}/{json_file_name}", "w") as of:
            json.dump(attacked_json, of, indent=4)

## ------------------------------------------------------------

if __name__ == '__main__':

    perform_attack(
        input_dir = "./synthetic-data/json/2020/01",
        output_dir ="./attacked-data/insert_one_event/2020/01",
        attack = Attack.INSERT_ONE_EVENT,
        parameters = {
            "frequency": (1, 1),
            "alarm_meas": (190.1, 200.1),
            "attack_lenght": (5, 10),
            "attack_start": (0, 100)
            }
        )

    perform_attack(
        input_dir="./synthetic-data/json/2021/01",
        output_dir="./attacked-data/modify_x_to_event/2021/01",
        attack=Attack.MODIFY_X_TO_EVENT,
        parameters= {
            "alarm_meas": (200.1, 200.1),
            "attack_lenght": (10, 10),
            "attack_start": (10, 10)
        }
    )

    perform_attack(
        input_dir="./synthetic-data/json/2021/03",
        output_dir="./attacked-data/modify_x_to_zero/2021/03",
        attack=Attack.MODIFY_X_TO_ZERO,
        parameters= {
            "attack_start": (0, 144),
            "attack_lenght": (3, 27)
        }
    )
    
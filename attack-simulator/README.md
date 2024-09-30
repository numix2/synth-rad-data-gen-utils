# Attacked data generator
This software takes as input real or synthetically generated radiation measurement data in a JSON format, and outputs another JSON formated file with the measurements in it, as if those measurements were captured during an attack on the system.

The aim of this application is to provide a way for researchers for generating large numbers of attacked data samples on which AI models can be tought.

## Possible attacks:
### Creating alarm where there wasn't one
| Attack | Situation | Parameters |
|---|---|---|
| INSERT_ONE_EVENT| The attacker either <ul><li>broadcasts false values to the sever,</li><li>or modifies the message before it gets to the sever</li></ul> | <ol><li>frequencie of attack (number of seconds between attacks)</li><li>value of attack</li><li>How long is the attack</li><li>when does the attack start</li></ol>|
| MODIFY_X_TO_EVENT | The attacker catches the message and modifies measurement data already present in it | <ol><li>The value of the attack</li><li>Number of measuements to modify</li><li>Where to start in the gile</li></ol>|

### Obscuring real alarm
| Attack | Situation | Parameters |
| --- | --- |---|
| MODIFY_X_TO_ZERO | The attacker captures a message with an alarm in it, and overwrites the alarm with zeros | <ol><li>Where to start the attack</li><li>how long is the attack</li></ol> |
| MODIFY_X_TO_MEAN | THe attacker captures a message with an alarm in it, and gets the mean of the measurements before the alarm, and overwrites the alarm with this mean value | <ol><li>Where to start the attack</li><li>how long is the attack</li></ol> |
| MODIFY_WITH_PAST_PATTERN | The attacker caputers a message with an alarm in it, and overwrites the alarm with a pattern that is taken from the previous measuements in the file. | <ol><li>Where the alarm starts</li><li>how long is the alarm</li></ol> |
| MODIFY_WITH_OWN_PATTERN | The attacker caputers a message with an alarm in it, and overwrites the alarm with a pattern that he creates. | <ol><li>Where the alarm starts</li><li>how long is the alarm</li><li>the pattern</li></ol> |
| MODIFY_WITH_GENERATED | The attacker captures a message with an alarm in it, and overwrites this alarm with synthetically generated data | <ol><li>Where the alarm starts</li><li>How long is the alarm</li></ol> |

## Usage
### Prerequisites
You have to have your input data in the format defined in `./Data format proposal`. You can synthetically generate radiation data in this format using either the `sensor-imitator` or the `standalone` generators in this repo; or if you have your own data you can use the `data_to_json.py` script to create the JSON formated document from it.

### Generating attacked data
If you have your input data, you can call the `perform_attack()` function with different arguments, to generate the desired outputs:
```python
# This attack will get the files found in ./synthetic-data/json/2020/01 folder, 
# and put all of the files found in it through the attack generator.
# The attacked files will be created at the location designated by output_dir=
#
# The attack that will be performed is the inser_one_event attack
#
# When defining the attack parameters you allways have to use a tuple
# The first member of the tuple is the lower bound of the attack
# The second is the upper bound
#
# If you wish that all files get the exact same attack, you should 
# give the upper and lower bounds as equal like here with attack_lenght
perform_attack(
    input_dir = "./synthetic-data/json/2020/01", 
    output_dir ="./attacked-data/insert_one_event/2020/01", 
    attack = Attack.INSERT_ONE_EVENT, 
    parameters = {
        "frequency": (1, 1),
        "alarm_meas": (190.1, 200.1),
        "attack_lenght": (10, 10),
        "attack_start": (0, 100)
        }
    )

perform_attack(
    input_dir = "./synthetic-data/json/2020/01", 
    output_dir ="./attacked-data/modify_with_own_pattern/2020/01", 
    attack = Attack.MODIFY_WITH_OWN_PATTERN, 
    parameters = {
        "attack_lenght": (10, 15),
        "attack_start": (0, 100),
        "pattern": [199.0, 199.1, 199.2, 199.1]
        }
    )
```
The reason for using tuples with lower and upper bounds is that we want to generate trainig data for an AI. Naturally gathered data would be somewhat random, so the generated data also benefits from being somewhat random. To this end, if different lower and upper bounds are given: for each attacked input file, the attack will be random lenght, have a random start point, and other parameters, between the given bounds of course.
# Synthetic radiation data generation standalone version

Repo for downloading and generating synthetic radiation data

Source of real data: http://omosjer.reak.bme.hu/


## Using the application
All major components of the framework contains the following:
- A configuration `.ini` file
- A python script

### Getting real data
If you don't already have real data to train the model with, you can find a script called `omosjer_download.py` in the `example` folder that query radiation measurements from OMOSJER (Hungarian Higher Educational Radiation Monitoring System). 

In its config file `download.ini` you can set the download folder, and parametrize the query.

Example for `download.ini`:
```ini
[folders]
output_folder = ../data/download/omosjer/

[parameters]
first_year = 2017
first_month = 1
last_year = 2023
last_month = 1
stations = [
    "budapestbme",
    "budapestsote",
    "budapestelte",
    "debrecen",
    "godollo",
    "kaposvar",
    "pecs",
    "veszprem",
    "sopron",
    "szeged1",
    "szeged2",
    "szekesfehervar",
    "szombathely"
    ]
```


### Preparing the data
If you have your data in many separate files, you can create one file containing all your data with the `prepare_training_data.py` script. You should use the `prepare.ini` file, to give an input and output folder, and the list of names of the input files. 

Example for `prepare.ini`:
```ini
[folders]
input_folder = ./data/download/omosjer/
output_folder = ./data/prepared/omosjer/

[files]
output_file_name = omosjer-prepared.csv
files_to_convert = [
    "budapestbme_2017-1-1_2017-1-31.csv",
    "budapestbme_2017-3-1_2017-3-31.csv"
    ]
```

### Training the model
If you have your training data prepared, you can run the `train.py` script to train the model, and create a `.tar` file containing said model and the corresponding scaler. The scaler is necessary, because by default ydata-synthetic generates data between 0 and 1, and we use this scaler, which gets initailized with the original training data,to scale the generated data to the domain of the original data. You should use the `train.ini` file to configure the training.

Example for `train.ini`:
```ini
[files]
input_data_file = ./data/prepared/omosjer/omosjer-prepared.csv
model_output_file = ./models/omosjer/omosjer-model.pkl

[gan_args]
batch_size = 128
learning_rate = 5e-4
noise_dim = 32
layers_dim = 128
beta_1 = 0
beta_2 = 1
data_dim = 1

[other_args]
hidden_dim = 144
seq_len = 144
n_seq = 1
gamma = 1

[train]
train_steps = 500


[train-data-properties]
time-step-minutes = 10
```
You can find more information on how to parametrize the training at the following sources:

[Modeling and Generating Time-Series Data using TimeGAN](https://towardsdatascience.com/modeling-and-generating-time-series-data-using-timegan-29c00804f54d)

[Time series generative adversarial networks paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/c9efe5f26cd17ba6216bbe2a7d26d490-Paper.pdf)

If you want to train a model on multi dimensional input, you need to set the `n_seq` variable to be equal to the number of dimensions:

```ini
[files]
input_data_file = ./data/prepared/omosjer/omosjer-prepared.csv
model_output_tar = ./models/omosjer/omosjer-model.tar

[gan_args]
batch_size = 128
learning_rate = 5e-4
noise_dim = 32
layers_dim = 128
beta_1 = 0
beta_2 = 1
data_dim = 1

[other_args]
hidden_dim = 144
seq_len = 144
n_seq = 2 # !!
gamma = 1

[train]
train_steps = 500

[train-data-properties]
time-step-minutes = 10
```

Models train this way will produce mutli-dimensional outputs as well, whitout the need to modify the generating script. If you want to try it out, you can find an example for a multi-dimensional `.csv` file at `.data/download/one-weather/archive_results_1645.csv`. However **this is an artificially inflated file** (its values have been copy-pasted a bunch of times) so **the model trained on this file wont produce usable synthetic data.**

### Generating synthetic data
If you have the trained model in a `.tar` file, you can use the `synth_data_generator.py` script, to generate your synthetic data. You should use the `generator.ini` file to give the script the model you want to use. The second thing that must be specified in the `generator.ini` file is the list of output files. You can name the output files anything as long as they are `.txt` files, but it is advised to name them with the name (or number) of the "device" which made the "measurement", becouse this way the output can be used as input for the JSON generating scripts without changes. 

Example for `generator.ini`:
```ini
[files]
model_tar = ./omosjer-model.tar
output_files = [
    "./data/generated/omosjer/0.txt",
    "./data/generated/omosjer/1.txt",
    "./data/generated/omosjer/2.txt",
    "./data/generated/omosjer/3.txt",
    "./data/generated/omosjer/4.txt",
    "./data/generated/omosjer/5.txt",
    "./data/generated/omosjer/6.txt",
    "./data/generated/omosjer/7.txt",
    "./data/generated/omosjer/8.txt",
    "./data/generated/omosjer/9.txt",
    "./data/generated/omosjer/10.txt",
    "./data/generated/omosjer/11.txt"
    ]
```

### Comparing the generated data with the original
If you have generated some synthetic data, you can compare it to the real data that the model was trained on. To do this use the `compare_synth_data.py` script. This will generate plots of both datasets. You should use the `compare.ini` file to give the script the two datasets to compare.

Example for `compare.ini`:
```ini
[files]
synth_data_file_path = ./data/generated/omosjer/0.txt
original_data_file_path = ./data/prepared/omosjer/prepared-omosjer.csv
```

## Creating JSON structure from the generated data
Once you have a file with your generated synthetic data in it, you can use the `data_to_json.py` script to generate a structured json file from it that conforms to the specification given in `../Data format Proposal/`. You should use the `data_to_json.ini` file to set up your initial parameters. 

This JSON format is used for storing real measurement data in a structured way and so it requres aditional parameters other than the generated synthetic data. By filling in the below `.ini` file, you give the json-creator script the parameters of the theoretical measurement device that "measured" the synthetic data. In order to differentiate real data from synthetic data, it is advised to us the JSON format's `labels` field to mark the data as synthetic. You can find more information about this JSON format in the specification, however for the generation the `start_date` and `time_incerment` variables demand explanation:

- `start_date`: here you must specify the time in ISO8601 format. This is the time the imagined measuring device started the measurement.
- `time_increment`: this variable tells the JSON creator script how many minutes have passed between the "measuring" of each syntheticly generated value in the input file.

For every input file, the script generates a json file which has the nameing scheme `<device>-<type>.json`

Please note that if the specification says about a variable that it is optional, then specifiing it in the `data_to_json.ini` file is also optional.

Example for `data_to_json.ini`:
```ini
[main]
version = 1
labels = [
    "synthetic"
    ]

[payload]
start_date = 2024-01-30T23:12:54Z
time_increment = 10
loc_lon = 40.2
loc_lat = 35.6
type = rad_dr
unit = nSv/h

[files]
output_dir = ./data/json/omosjer
input_files = [ 
    "./data/generated/omosjer/1.txt",
    "./data/generated/omosjer/2.txt",
    "./data/generated/omosjer/3.txt",
    "./data/generated/omosjer/4.txt",
    "./data/generated/omosjer/5.txt",
    "./data/generated/omosjer/6.txt",
    "./data/generated/omosjer/7.txt",
    "./data/generated/omosjer/8.txt",
    "./data/generated/omosjer/9.txt",
    "./data/generated/omosjer/10.txt",
    "./data/generated/omosjer/11.txt"
    ]
```

## Validating your JSON file
Once you have your json file with your generated synthetic data in it, you can validate the json structure, using the `json_schema_check.py` script, with the `data-format_schema.json` file found in `./Data format proposal/v2.1/`. You should use the `validate.ini` file to give your json file and the schema to the script

Example for `validate.ini`:
```ini
[files]
schema_file = ./Data\ format\ proposal/v2.1/data-format_schame.json
json_file = ./data/json/omosjer/1-rad_dr.json
```

# RDS sensor imitator
This application is a synthetic sensor. It takes a "seed" and form that it generates synthetic data. It then transimts this synthetic data in a manner similar to a real measurement sensor, thus imitating it. 

## Using the application
### Createing seeds
A seed is a `.tar` archive, which has the trained generator modell in it, and all other suplementary data that is required for data generation. To create a seed you can use the scrip found in the `model-training` folder. Following is an example how to craete a seed:

- Firstly you have to have training data, in csv format. The example of this is in the model-training/training_data folder.
```csv
Date,Value
2017-01-01 00:20:00,89.34
2017-01-01 00:10:00,88.21
2017-01-01 00:30:00,89.9
2017-01-01 00:40:00,90.45
2017-01-01 00:50:00,89.23
2017-01-01 01:00:00,87.05
2017-01-01 01:10:00,89.1
2017-01-01 01:20:00,89.13
2017-01-01 01:30:00,88.94
2017-01-01 01:40:00,86.25
2017-01-01 01:50:00,89.49
...
```
This is data we got from a real background radiation senser.

- If you have the training data you can set training parameters in the `train.ini` file:
```ini
[files]
input_data_file = ./training_data/budapestbme_2017.csv
model_output_tar = ../model-seeds/rds.tar

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
#n_seq = 2
gamma = 1

[train]
train_steps = 2

[train-data-properties]
time-step-minutes = 10
```
To understand the training parametrization, here are some resources for the ydata-synthetic library:

[Modeling and Generating Time-Series Data using TimeGAN](https://towardsdatascience.com/modeling-and-generating-time-series-data-using-timegan-29c00804f54d)

[Time series generative adversarial networks paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/c9efe5f26cd17ba6216bbe2a7d26d490-Paper.pdf)

### Using the sensor
If you have your seed, you can initialize and start the sensor. The sensor while in use, will transmit the data in the JSON format specified in `/Data format proposal`.

To initialize the sensor you have to set the following parameters in the `sensor.py`:
```python
MODEL_TAR_PATH = "../sensor-seeds/rds1.tar"
RUNTIME = 0.5 # hours
LOC_LON = 40.2
LOC_LAT = 35.6
TYPE = "rad_dr"
UNIT = "nSv/h"
DEVICE = 27
OUTPUT_LOCATION = "./test"
SERVER_IP = "http://localhost:8000"
```
The `SERVER_IP` is the ip address of the sever to which the sensor will transmit the data. An example implementation can be found in `server_mockup.py`.
"""
This module is responsible for training and creating the seed 
that will be used for synthetic data generation
"""

from configparser import ConfigParser
from ydata_synthetic.synthesizers.timeseries.timegan.model import TimeGAN
from ydata_synthetic.synthesizers import ModelParameters
from ydata_synthetic.preprocessing.timeseries.utils import real_data_loading
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
import tarfile
import os
from io import BytesIO

parser = ConfigParser()
parser.read('train.ini')

SEQ_LEN = int(parser.get('other_args', 'seq_len'))
N_SEQ = int(parser.get('other_args', 'n_seq'))
HIDDEN_DIM = int(parser.get('other_args', 'hidden_dim'))
GAMMA = int(parser.get('other_args', 'gamma'))
NOISE_DIM = int(parser.get('gan_args', 'noise_dim'))
DIM = int(parser.get('gan_args', 'layers_dim'))
BATCH_SIZE = int(parser.get('gan_args', 'batch_size'))
LEARNING_RATE = float(parser.get('gan_args', 'learning_rate'))
BETA_1 = int(parser.get('gan_args', 'beta_1'))
BETA_2 = int(parser.get('gan_args', 'beta_2'))
DATA_DIM = int(parser.get('gan_args', 'data_dim'))
TRAIN_STEPS = int(parser.get('train', 'train_steps'))
TIME_STEP_MINUTES = int(parser.get('train-data-properties', 'time-step-minutes'))

file_path = parser.get('files', 'input_data_file')
rds_df = pd.read_csv(file_path)

try:
    rds_df = rds_df.set_index('Date').sort_index()
except:
    rds_df=rds_df
    print('No date')


rds_data = real_data_loading(rds_df.values, seq_len=SEQ_LEN)

print(len(rds_data), rds_data[0].shape)

gan_args = ModelParameters(
    batch_size=BATCH_SIZE,
    lr=LEARNING_RATE,
    noise_dim=NOISE_DIM,
    layers_dim=DIM
    )

synth = TimeGAN(
    model_parameters=gan_args,
    hidden_dim=HIDDEN_DIM,
    seq_len=SEQ_LEN,
    n_seq=N_SEQ,
    gamma=GAMMA
    )

synth.train(rds_data, train_steps=TRAIN_STEPS)
synth.save('model.pkl')
scaler = MinMaxScaler().fit(rds_df.values)


archive = tarfile.open(parser.get('files', 'model_output_tar'), mode='w')
archive.add("model.pkl")
os.remove('model.pkl')

# save scaler
scaler_pickle = pickle.dumps(scaler)
scaler_pickle_bytes = BytesIO()
scaler_pickle_bytes.write(scaler_pickle)
scaler_pickle_bytes.seek(0)
tarinfo = tarfile.TarInfo(name="scaler.pkl")
tarinfo.size = len(scaler_pickle_bytes.getvalue())
archive.addfile(tarinfo=tarinfo, fileobj=scaler_pickle_bytes)

# save time-step + batch_size + seq_len + n_seq
needed_data = {}
needed_data["time_step"] = TIME_STEP_MINUTES
needed_data["batch_size"] = BATCH_SIZE
needed_data["sequence_lenght"] = SEQ_LEN
needed_data["data_dim"] = N_SEQ

time_step_pickle = pickle.dumps(needed_data)
time_step_bytes = BytesIO()
time_step_bytes.write(time_step_pickle)
time_step_bytes.seek(0)
time_step_tarinfo = tarfile.TarInfo(name="other.pkl")
time_step_tarinfo.size = len(time_step_bytes.getvalue())
archive.addfile(tarinfo=time_step_tarinfo, fileobj=time_step_bytes)

archive.close()

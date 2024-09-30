"""
This module uses the trained seed, to generate syntethic data.
"""

from configparser import ConfigParser
from sklearn.preprocessing import MinMaxScaler
from ydata_synthetic.synthesizers.timeseries import TimeGAN
import pandas as pd
import json
import tarfile
import pickle

parser = ConfigParser()
parser.read('generator.ini')

#model_file = parser.get('files', 'model_file')

archive = tarfile.open(parser.get('files', 'model_tar'))
try:
    model_pickle = archive.extractfile('model.pkl')
    if model_pickle is not None:
        synth = TimeGAN.load(model_pickle)

        scaler_pickle = archive.extractfile('scaler.pkl')
        if scaler_pickle is not None:
            scaler = pickle.load(scaler_pickle)

            outputs = json.loads(parser.get('files', 'output_files'))


            for output_file in outputs:

                synth_data = synth.sample(1)

                synth_data = scaler.inverse_transform(synth_data[0])


                with open(output_file, 'w') as of:
                    synth_data.tofile(of, sep='\n', format='%0.2f')
finally:
    archive.close()

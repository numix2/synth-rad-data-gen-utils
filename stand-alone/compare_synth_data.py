"""
This module generates plots from the given real data and synthetic data
"""

from configparser import ConfigParser
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from ydata_synthetic.synthesizers.timeseries.timegan.model import TimeGAN
import numpy as np
import pandas as pd

parser = ConfigParser()
parser.read('compare.ini')

synth_data_file_path = parser.get('files', 'synth_data_file_path')
original_data_file_path = parser.get('files', 'original_data_file_path')

rds_df = pd.read_csv(original_data_file_path)

try:
    rds_df = rds_df.set_index('Date').sort_index()
except:
    rds_df=rds_df
    print('No date')

print('Mean: ', np.mean(rds_df.values[0:143]))
plt.plot(rds_df.values[0:143])
plt.title('Original data')
plt.xlabel('Time [10 min]')
plt.ylabel('Detected radioation [nSv/h]')
plt.ylim(0, 100)
plt.show()


synth_data = []
with open(synth_data_file_path, 'r') as sdf:
    for line in sdf:
        line = line.strip()
        synth_data.append([float(line)])

plt.plot(synth_data)
plt.title('Synthetic data')
plt.xlabel('Time [10 min]')
plt.ylabel('Detected radioation [nSv/h]')
plt.ylim(0, 100)
plt.show()
print('Mean: ', np.mean(synth_data))

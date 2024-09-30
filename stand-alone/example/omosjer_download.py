"""
This module downloads real data from the omosjer
"""
import calendar
from configparser import ConfigParser
import json
import requests

parser = ConfigParser()
parser.read('download.ini')

stations = json.loads(parser.get('parameters', 'stations'))
download_directory = parser.get('folders', 'output_folder')

firstYear = int(parser.get('parameters', 'first_year'))
firstMonth = int(parser.get('parameters', 'first_month'))
lastYear = int(parser.get('parameters', 'last_year'))
lastmonth = int(parser.get('parameters', 'last_month'))

periods = []
for year in range(firstYear, lastYear+1):
    for month in range(firstMonth, 12+1):
        if year == lastYear and month > lastmonth:
            print(year, month)
            break
        periods.append({'from': str(year) + '-' + str(month) + '-' + '1', 'till': str(year) + '-' + str(month) + '-' + str(calendar.monthrange(year, month)[1])})

print('Starting download...')

for station in stations:
    for period in periods:
        payload = {'station': station, 'period': 'period', 'from': period['from'], 'till': period['till']}
        r = requests.get('http://omosjer.reak.bme.hu/drawgraph.php', params=payload)
        print('Next URL: ', r.url)
        lines = r.text.split('<BR>')
        lines[0] = lines[0].split('>')[1] # omit the font tag from first line
        lines = lines[:-1] # omit the last line containing only </font>
        fileName = download_directory + station + '_' + period['from'] + '_' + period['till'] + '.csv'
        print('Filename to save data: ' + fileName)
        with open(fileName, 'w') as f:
            for line in lines:
                data = line.split()
                f.write(data[0] + ',')
                f.write(data[1] + ',')
                f.write(data[4])
                if data[5] != 'nSv/h' :
                    f.write(',' + data[5])
                    print('Not nSv/h in ', fileName)
                f.write('\n')

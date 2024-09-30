"""
This module takes the cvs files given in the prepare.ini file, 
and from them creates the input for the training of the AI
"""
from configparser import ConfigParser
import json

parser = ConfigParser()
parser.read('prepare.ini')

input_directory = parser.get('folders', 'input_folder')
output_directory = parser.get('folders', 'output_folder')

files = json.loads(parser.get('files', 'files_to_convert'))
output_file = parser.get('files', 'output_file_name')

outputFile = output_directory + output_file

with open(outputFile, 'w') as outf:
    outf.write('Date,Value\n')
    for fileName in files:
        with open(input_directory + fileName, 'r') as inf:
            for line in inf:
                #outf.write(line.split(',')[2]) # if only the measurements are required
                #outf.write(line) # if the whole record is required
                data = line.split(',')
                outf.write(data[0] + ' ')
                outf.write(data[1] + ',')
                outf.write(data[2])
                #outf.write('\n')

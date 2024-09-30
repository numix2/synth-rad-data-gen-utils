"""
This modul is for checking if the given json file satisfies the given json schema.
The two arguments are:
    - schema: The path to the schema file we are checking against
    - json_file: the path to the json file we are checking
"""

from configparser import ConfigParser
import json
from jsonschema import validate


parser = ConfigParser()
parser.read('validate.ini')
SCHEMA_FILE = parser.get('files', 'schema_file')
JSON_FILE = parser.get('files', 'json_file')

with open(JSON_FILE, "r") as jf:
    jf_instance = json.load(jf)

with open(SCHEMA_FILE, "r") as sc:
    jf_schema = json.load(sc)

validate(instance=jf_instance, schema=jf_schema)

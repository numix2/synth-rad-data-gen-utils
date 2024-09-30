import argparse
import pprint

from n42_xml import write, create_N42
from json_parser import parse_json

parser = argparse.ArgumentParser(
    prog="N42 format generator",
    description="Convert own json measurement format to N42 format"
)
parser.add_argument("jsonfilename", help="The path to the json file")
parser.add_argument("outputlocation", help="The path to the output location")
args = parser.parse_args()

parsed_json = parse_json(args.jsonfilename)
pprint.pprint(parsed_json)
xml_out = create_N42(parsed_json)
write(xml_out, args.outputlocation)


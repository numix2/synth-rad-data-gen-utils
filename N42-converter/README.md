# JSON to N42 converter

The purpose of this python application is to convert our JSON format documents to ANSI N42.42-2012 format.

It takes in one JSON file, and produces one N42 formated XML for each different `"device"` attribute. This is necessary becouse the JSON format allows for different devices to be present in the same file while N42 only permits one device per file. The outputed XML files are of the following form: `<device_name>.xml`
## Components

- `n42_convert.py`: this file is the main executable of the application. It takes two command line arguments.
- `json_parser.py`: This file contains the functions that convert the JSON file into a dictionary of lists, which is the input for the N42 builder.
- `n42_xml.py`: This file contains the functions and enums that convert the input into an N42 format XML document.

## Usage

`n42_convert.py` is the main executable of the application. It takes two command line arguments:
```dotnetcli
python n42_conver.py <path_to_json> <path_to_output_dir>
```

Example:
```dotnetcli
python n42_convert.py ./home/example.json ./home
```
**Please note**: To be compliant with the N42 standard, the output file has to have `.n42` extension, but I used `.xml` in the examples, so that the reuslting file has syntax highlighting in an editor.



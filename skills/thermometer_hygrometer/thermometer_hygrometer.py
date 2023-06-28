# UNIMPLEMENTED - STUB

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--get', action='store_true', help='Query the information from the thermometer/hygrometer combo.')

args = parser.parse_args()

output = {"temperature": "unknown", "humidity": "unknown"}

if args.get:
    # +-------------------------------+
    # |Accessor implementation here  |
    # +-------------------------------+
    output = {"temperature": 72, "humidity": 55}  # hardcoded stub
    
print(output)

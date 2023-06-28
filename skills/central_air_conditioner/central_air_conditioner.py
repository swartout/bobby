# UNIMPLEMENTED - STUB

import argparse

def temperature_range(value):
    if 60 <= int(value) <= 90:
        return value
    else:
        raise argparse.ArgumentTypeError(f"Temperature must be between 60 and 90, inclusive.")

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['cool', 'heat', 'fan'], help='The mode that the air conditioner will use to affect the climate.')
parser.add_argument('--temperature', type=temperature_range, help='The target ambient temperature that the air conditioner will attempt to reach, in Fahrenheit.')
parser.add_argument('--get', action='store_true', help='Query the information from the air conditioner.')

args = parser.parse_args()

output = {"mode": "unchanged", "temperature": "unchanged"}

if args.get:
    # +-----------------------------+
    # |Accessor  implementation here|
    # +-----------------------------+
    output = {"mode": "cool", "temperature": 69} # hardcoded stub
    
else:
    if args.mode:
        output["mode"] = args.mode

    if args.temperature:
        output["temperature"] = int(args.temperature)

    # +---------------------------+
    # |Mutator implementation here|
    # +---------------------------+

print(output)

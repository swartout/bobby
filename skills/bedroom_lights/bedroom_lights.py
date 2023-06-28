# UNIMPLEMENTED - STUB

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['on', 'off'], help='The mode for the bedroom lights (on/off).')
parser.add_argument('--get', action='store_true', help='Query the information from the lights.')

args = parser.parse_args()

output = {"mode": "unchanged"}

if args.get:
    # +-----------------------------+
    # |Accessor implementation here |
    # +-----------------------------+
    output = {"mode": "on"}  # hardcoded stub
    
else:
    if args.mode:
        output["mode"] = args.mode

    # +---------------------------+
    # |Mutator implementation here|
    # +---------------------------+

print(output)

import os
import json
import logging
from ntc_templates.parse import parse_output

def parse_data(file_path):
    raw_dir = file_path
    structured_dir = os.path.join('data', 'structured')
    os.makedirs(structured_dir, exist_ok=True)

    commands = [
        'show version',
        'show ip interface brief',
        'show inventory'
    ]

    parsed_results = {}
    for cmd in commands:
        filename = f"{cmd.replace(' ', '_')}.txt"
        raw_file_path = os.path.join(raw_dir, filename)
        if not os.path.exists(raw_file_path):
            logging.info(f"[PARSE_FAIL]: {cmd}")
            print(f"Raw file for '{cmd}' not found at {raw_file_path}.")
            continue
        try:
            with open(raw_file_path, 'r', encoding='utf-8') as f:
                raw_data = f.read()

            command_data = parse_output(platform="cisco_ios", command=cmd, data=raw_data)
            if command_data and isinstance(command_data, (list, dict)) and len(command_data) > 0:
                struct_filename = f"{cmd.replace(' ', '_')}.json"
                struct_file_path = os.path.join(structured_dir, struct_filename)
                with open(struct_file_path, 'w', encoding='utf-8') as sf:
                    json.dump(command_data, sf, indent=4)
                parsed_results[cmd] = command_data
                logging.info(f"[PARSE_OK]: {cmd}")
                print(f"Successfully parsed and validated {cmd}")
            else:
                logging.info(f"[PARSE_FAIL]: {cmd}")
                print(f"Parsing returned empty or invalid structure for: {cmd}")
        except Exception as e:
            logging.info(f"[PARSE_FAIL]: {cmd}")
            print(f"Error parsing command '{cmd}': {e}")

    return parsed_results
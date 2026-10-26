import os
import logging

def collect_data(connection):
    output_dir = os.path.join('data', 'raw')
    os.makedirs(output_dir, exist_ok=True)

    commands = [
        'show version',
        'show ip interface brief',
        'show inventory'
    ]

    for cmd in commands:
        try:
            output = connection.send_command(cmd)
            logging.info("[CMD_RUN]: %s", cmd)
            file_path = os.path.join(output_dir, f"{cmd.replace(' ', '_')}.txt")
            with open(rf"{file_path}", 'w', encoding='utf-8') as f:
                f.write(output)

            print(f"successfully executed and saves: {cmd} -> {file_path}")
        except Exception as e:
            print(f"failed to execute and save: {cmd} -> {e}")
import logging
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException

def connect(host, username, password):
    device = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password
    }
    try:
        connection = ConnectHandler(**device)
        prompt_banner = connection.find_prompt()
        logging.info("[CONNECT_OK]")
        print(f"Successfully connected to {host}. Banner/Prompt: {prompt_banner}")
        return connection

    except (NetmikoTimeoutException, NetmikoAuthenticationException, SSHException) as e:
        logging.info("[CONNECT_FAIL]")
        print(f"Connection failed for {host} due to network/auth error: {e}")
        return None

    except Exception as e:
        logging.info("[CONNECT_FAIL]")
        print(f"An unexpected error occurred while connecting to {host}: {e}")
        return None
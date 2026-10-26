import getpass
import logging

def prompt():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    logging.info("[CREDENTIALS_COLLECTED]")
    print("Credentials successfully collected and logged.")
    return username, password
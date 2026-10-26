import logging
from pathlib import Path

from Functions.collect import collect_data
from Functions.netmiko import connect
from Functions.parse import parse_data
from Functions.prompt import prompt
from Functions.report import generate_report

log_path = Path(__file__).resolve().parent / "logs" / "lab.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    """
    Orchestrates the end-to-end network automation workflow:
    Credentials -> SSH Connection -> Data Collection -> Parsing -> Reporting
    """
    print("=== Starting Network Automation Workflow ===")
    
    username, password = prompt()
    
    host = input("Enter device IP/Host: ")
    
    connection = connect(host=host, username=username, password=password)
    
    if connection:
        try:
            collect_data(connection)
            
            parse_data(file_path='data/raw')

            generate_report()
            
        finally:
            connection.disconnect()
            print("SSH connection closed successfully.")
    else:
        print("Workflow halted due to connection failure.")

if __name__ == "__main__":
    logging.info("[LAB2-START]")
    print("[LAB2-START] Lab 2 execution initiated.")
    try:
        main()
    finally:
        logging.info("[LAB2-END]")
        print("[LAB2-END] Lab 2 execution finished.")
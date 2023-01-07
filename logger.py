class Logger:
    def __init__(self):
        self.logs = []
        
    def log(self, message):
        self.logs.append(message)
        print(message)
        
    def get_logs(self):
        return self.logs
# Set up a logging object
import logging
import os

cwd = os.getcwd()

logging.basicConfig(
    level=logging.DEBUG,
    filename=f"comp/parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

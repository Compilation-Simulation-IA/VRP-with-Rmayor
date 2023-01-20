class Logger:
    def __init__(self):
        self.logs = []
        
    def log(self, message):
        self.logs.append(message)        
        
    def get_logs(self):
        return self.logs
import os
import atexit
from enum import Enum
from datetime import datetime

LogLocation = "logs/"
MAX_LOGS = 10

class LogLevel(Enum):
    INFO = 1 # General informational messages about the program's execution, such as loading mods, processing cards, etc.
    WARNING = 2 # Non-critical issues that may indicate a problem or potential issue, such as missing card data, invalid mana cost characters, etc.
    ERROR = 3 # Critical issues that may cause the program to malfunction or produce incorrect results, such as failure to load a mod, failure to save a log file, etc.
    TERMINAL = 4 # Terminal errors that require the program to exit immediately, such as unrecoverable errors, security issues, etc. When a terminal error is logged, the logger will save the log file and then exit the program with an error message.

class logger:
    '''
    A simple logger class that can be used to log messages to a file. This is used for debugging purposes and to keep track of any errors that may occur during the execution of the program.
    '''
    def __init__(self, LogHeader: str):
        self.LogHeader = LogHeader
        self.logContent = ""
        atexit.register(self.saveLog)

    
    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        '''
        Logs a message to the log content with the specified log level.

        Args:
            message (str): The message to log.
            level (LogLevel, optional): The log level of the message. Defaults to LogLevel.INFO.
        '''
        self.logContent += f"[{level.name}]-{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}: {message}\n"

        if level == LogLevel.TERMINAL:
            self.saveLog()
            exit("Terminal Error Occurred. Check log file for details.")
    
    def saveLog(self):
        '''
        Saves the log content to a file in the logs directory. The filename is generated based on the log header and the current date and time.
        '''
    
        #Create logs directory if it doesn't exist
        if not os.path.exists(LogLocation):
            os.makedirs(LogLocation)

        #Generate filename based on log header and current date and time
        filename = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
        filepath = os.path.join(LogLocation, filename)

        #Save log content to file
        with open(filepath, "w") as f:
            f.write(f"---{self.LogHeader}---\n\n")
            f.write(self.logContent)

        #Enforce max log count - delete oldest if over limit
        logs = sorted(
            [f for f in os.listdir(LogLocation) if f.endswith(".log")],
            key=lambda f: os.path.getmtime(os.path.join(LogLocation, f))
        )
        while len(logs) > MAX_LOGS:
            os.remove(os.path.join(LogLocation, logs.pop(0)))


if __name__ == "__main__":
    MSElogger = logger("MSE Mod Loader")
    MSElogger.log("This is an info message.")
    MSElogger.log("This is a warning message.", LogLevel.WARNING)
    MSElogger.log("This is an error message.", LogLevel.ERROR)
    MSElogger.log("This is a terminal message.", LogLevel.TERMINAL)

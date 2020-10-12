import os
import json
import logging

class LocalFormatter(logging.Formatter):
    def __init__(self):
        super(LocalFormatter, self).__init__(
            fmt='%(asctime)s %(process)-5d %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

class Logger(logging.Logger):
    """
    This is the custom logging module
    """

    __instance = None

    def __init__(self):
        self._formatter = None
        if Logger.__instance is not None:
            raise Exception("Logger already in use.")
        else:
            super(Logger, self).__init__(name="logger")
            self._set_file_handler()
            self._set_stream_handler()
            self._set_logging_level()
            Logger.__instance = self

    def _set_file_handler(self):
        handler = logging.FileHandler("log.log")
        formatter = LocalFormatter()
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def _set_stream_handler(self):
        sh = logging.StreamHandler()
        formatter = self._get_stream_formatter()
        sh.setFormatter(formatter)
        self.addHandler(sh)

    def _set_logging_level(self):
        logging_level_env = os.getenv("LOGLEVEL", default="INFO")
        if logging_level_env == "DEBUG":
            self.setLevel(logging.DEBUG)
        elif logging_level_env == "INFO":
            self.setLevel(logging.INFO)
        elif logging_level_env == "WARN":
            self.setLevel(logging.WARN)
        elif logging_level_env == "ERROR":
            self.setLevel(logging.ERROR)
        else:
            raise ValueError(f"Logging level must be DEBUG, INFO, WARN or ERROR, got {logging_level_env} instead.")

    @staticmethod
    def _get_stream_formatter():
        formatter_env = os.getenv("LOGFORMATTER", default="LOCAL")
        if formatter_env == "LOCAL":
            formatter = LocalFormatter()
        elif formatter_env == "STACKDRIVER":
            formatter = StackdriverFormatter()
        else:
            raise AttributeError("Wrong formatter passed, expected \"LOCAL\" or \"STACKDRIVER\", got \"{}\" instead.".format(formatter_env))
        return formatter

    @staticmethod
    def _get():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance


logger = Logger._get()
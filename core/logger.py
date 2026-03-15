import logging
import os
from core.qt_log_handler import QtLogHandler

class CutForgeLogger:

    def __init__(self):
        os.makedirs("data/logs", exist_ok=True)

        self.logger = logging.getLogger("cutforge")
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # file handler
        file_handler = logging.FileHandler("data/logs/cutforge.log")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

        # qt handler
        self.qt_handler = QtLogHandler()
        self.qt_handler.setFormatter(formatter)

        self.logger.addHandler(self.qt_handler)

    def get_logger(self):
        return self.logger
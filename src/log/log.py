import time


class LogManager:
    def __init__(self, log_path='logs/', filename_suffix=None):
        if filename_suffix is None:
            self.filename_suffix = time.strftime('_%Y%m%d%H%M%S')
        else:
            self.filename_suffix = filename_suffix

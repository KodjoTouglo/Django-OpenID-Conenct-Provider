import logging


class FilterLevels(logging.Filter):
    def __init__(self, filter_levels=None):
        super(FilterLevels, self).__init__()
        self._filter_levels = filter_levels

    def filter(self, record):
        if record.levelname in self._filter_levels:
            return True
        if record.getMessage().startswith('GET /'):
            return False
        return False


class FilterRequest(logging.Filter):
    def filter(self, record) -> bool:
        verb = ['GET /', 'POST /', 'PUT /', 'PATCH /', 'DELETE /']
        for i in verb:
            if i in record.getMessage():
                return False
        return True
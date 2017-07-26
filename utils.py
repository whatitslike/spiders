import logging


def get_logger(name):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(message)s')
    file_handler = logging.FileHandler('%s-spider.log' % name)
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger

import logging
from logging.handlers import RotatingFileHandler

logfile = 'logs.log'
log = logging.getLogger('my_log')
log.setLevel(logging.INFO)
fh = RotatingFileHandler(logfile, encoding='utf-8', maxBytes=2**20*5, backupCount=2)
basic_formater = logging.Formatter("%(asctime)s : [%(levelname)s] [%(lineno)d] : %(message)s")
fh.setFormatter(basic_formater)
log.addHandler(fh)

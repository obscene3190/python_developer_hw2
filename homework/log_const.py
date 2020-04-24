import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ex_log = logging.getLogger('Exception_Logger')
log = logging.getLogger('Logger')
ex_log.setLevel(logging.WARNING)
log.setLevel(logging.INFO)


fh1 = logging.FileHandler('ex_log.log', encoding='utf-8')
fh2 = logging.FileHandler('log.log', encoding='utf-8')
fh1.setFormatter(formatter)
fh2.setFormatter(formatter)

ex_log.addHandler(fh1)
log.addHandler(fh2)

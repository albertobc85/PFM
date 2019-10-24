import logging

formato_log = '%(LeveLname)s %(asctime)s - %(message)s'
logging.basicConfig(filename = "D:\Trabajo Fin de Master\logging.log",
                    level = logging.WARNING,
                    format = formato_log)
logger = logging.getLogger(__name__)
import logging


def logger():
    """
    Setup basic logging for console.

    Usage:
    	Initialize the logger by adding the code at the top of your script:
    	``logger = logger()``

    TODO: add log file export
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger

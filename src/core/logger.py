from logging import getLogger, Logger, INFO, Formatter, basicConfig


logger: Logger = getLogger()
basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger.setLevel(INFO)

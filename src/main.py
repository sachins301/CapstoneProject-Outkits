import pandas as pd
from pandas import DataFrame
import logging

from src.depopconnection import DepopConnection
from src.ebayconnection import EbayConnection
from src.mercariconnection import MercariConnection


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logging level
    # Create handlers
    file_handler = logging.FileHandler('../resources/outkitsapicall.log', mode='w', encoding='utf-8')
    # Create formatters and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(file_handler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    # Starting ebay connection
    ebayDf: DataFrame = pd.DataFrame()

    try:
        logger.info("Starting ebay connection")
        connection = EbayConnection(logger)
        ebayDf: DataFrame = connection.connect()
    except Exception as ex:
        logger.exception("Exception in ebay: %s", ex)

    # Mercari Connection
    try:
        logger.info("Starting Mercari connection")
        mercari_connection = MercariConnection(logger)
        mercari_connection.connect()
    except Exception as ex:
        logger.exception("Exception in Mercari", ex)

    # Depop Connection
    try:
        logger.info("Starting Mercari connection")
        depop_connection = DepopConnection(logger)
        depop_connection.connect()
    except Exception as ex:
        logger.exception("Exception in Depop", ex)

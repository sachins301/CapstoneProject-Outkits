import pandas as pd
from pandas import DataFrame

from src.ebayconnection import EbayConnection

import logging

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

    # Starting ebay connection
    ebayDf: DataFrame = pd.DataFrame()

    try:
        logger.info("Starting ebay connection")
        connection = EbayConnection(logger)
        ebayDf: DataFrame = connection.connect()
    except Exception as ex:
        logger.exception("Exception in ebay: %s", ex)
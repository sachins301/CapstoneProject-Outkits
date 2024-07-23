import os

import pandas as pd
from pandas import DataFrame
import logging
import sys

from src import commonutil
from src.depopconnection import DepopConnection
from src.ebayconnection import EbayConnection
from src.mercariconnection import MercariConnection
from src.poshmarkconnection import PoshmarkConnection

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logging level
    # Create handlers
    file_handler = logging.FileHandler('outkitsapicall.log', mode='w', encoding='utf-8')
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

    logger.info("Current working directory:"+ os.getcwd())
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    logger.info("Executable internal folder: "+ base_path)

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
        logger.info("Starting Depop connection")
        depop_connection = DepopConnection(logger)
        depop_connection.connect()
    except Exception as ex:
        logger.exception("Exception in Depop", ex)

    # Poshmark Connection
    try:
        logger.info("Starting Poshmark connection")
        poshmark_connection = PoshmarkConnection(logger)
        poshmark_connection.connect()
    except Exception as ex:
        logger.exception("Exception in Poshmark", ex)


    try:
        attachment_paths = ['outputebay.xlsx', 'outputmercari.xlsx', 'outputdepop.xlsx', 'outputposhmark.xlsx']
        commonutil.send_email(
            subject="Search Results for APIS",
            body="Please find attached the search results.",
            attachment_paths=attachment_paths
        )
    except Exception as ex:
        logger.exception("Failed to send email notification", ex)
    else:
        logger.info('Successfully sent the mail')

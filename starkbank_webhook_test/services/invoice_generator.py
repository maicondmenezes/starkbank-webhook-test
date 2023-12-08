import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from starkbank_webhook_test.constants import INPUT_DIR, OUTPUT_DIR, PRIVATE_KEY_PATH
from starkbank_webhook_test.starkbank_integration import (
    StarkbankIntegration,
    StarkbankIntegrationError,
)

# Constants for file paths
SETTINGS_FILE_PATH = os.path.join(
    INPUT_DIR, 'settings/invoices_generator_setup.json'
)
OUTPUT_MESSAGES_PATH = os.path.join(
    OUTPUT_DIR, 'messages/invoices_generator_messages.json'
)
LOG_FILE_PATH = os.path.join(OUTPUT_DIR, 'logs/invoice_generator_service.log')

# Setting up logger and handler for the InvoiceGeneratorService class
service_logger = logging.getLogger('InvoiceGeneratorService')
service_logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(
    LOG_FILE_PATH, when='midnight', backupCount=7
)
handler.setLevel(logging.DEBUG)
service_logger.addHandler(handler)


# Create a class for handling Invoice Generation
class InvoiceGeneratorService:
    @classmethod
    def create_engine(cls, settings_file_path: str, private_key_path: str):
        """
        Create a StarkbankIntegration instance.

        Args:
            - settings_file_path (str): Path to the configuration file.
            - private_key_path (str): Path to the private key file.
        """
        try:
            # Load the json object called 'engine' from the configuration file
            with open(settings_file_path, 'r') as settings_file:
                engine_config = json.load(settings_file).get('engine', {})

            # Load the private key from the specified file
            with open(private_key_path, 'r') as private_key_file:
                private_key = private_key_file.read()

            # Initialize StarkbankIntegration instance using 'engine' object and private key
            starkbank_integration = StarkbankIntegration(
                environment=engine_config.get('environment', 'sandbox'),
                id=engine_config.get('id', ''),
                private_key=private_key,
                auth_type=engine_config.get('auth_type', 'project'),
                webhook_url=engine_config.get('webhook_url', ''),
            )
            # Create a StarkbankIntegration instance
            return starkbank_integration
        except Exception as e:
            raise e

    def __init__(self, settings_file_path: str, private_key_path: str):
        """
        Initialize InvoiceGeneratorService with StarkbankIntegration instance.

        Args:
            - settings_file_path (str): Path to the configuration file.
            - private_key_path (str): Path to the private key file.
        """
        # Load params from the configuration file
        with open(settings_file_path, 'r') as settings_file:
            self.params = json.load(settings_file).get('params', {})

        try:
            self.engine = self.create_engine(
                settings_file_path, private_key_path
            )
        except Exception as e:
            service_logger.error(f'Engine creation error: {e}')
            raise e

    def run(self):
        """
        Run the invoice generation process using StarkbankIntegration instance.
        """
        try:
            # Connect to Stark Bank API for authentication
            self.engine.connect()

            # Run the invoice generation process
            self.engine.issue_random_invoices(self.params)

        except StarkbankIntegrationError as e:
            # Log any exception that occurs during invoice generation
            service_logger.error(f'Invoice generation error: {e}')
        finally:
            # Close the logger handler to flush any buffered logs
            for handler in service_logger.handlers:
                handler.close()
                service_logger.removeHandler(handler)

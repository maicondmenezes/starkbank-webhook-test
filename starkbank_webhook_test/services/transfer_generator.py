import json
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from requests.exceptions import RequestException

from starkbank_webhook_test.constants import INPUT_DIR, OUTPUT_DIR, PRIVATE_KEY_PATH
from starkbank_webhook_test.starkbank_integration import (
    Error,
    InvalidSignatureError,
    StarkbankIntegration,
    StarkbankIntegrationError,
)

# Constants for file paths
SETTINGS_FILE_PATH = os.path.join(
    INPUT_DIR, 'settings/transfer_generator_setup.json'
)
LOG_FILE_PATH = os.path.join(OUTPUT_DIR, 'logs/transfer_generator_service.log')


# Setting up logger and handler for the TransferGeneratorService class
service_logger = logging.getLogger('TransferGeneratorService')
service_logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(
    LOG_FILE_PATH, when='midnight', backupCount=7
)
handler.setLevel(logging.DEBUG)
service_logger.addHandler(handler)


class TransferGeneratorService:
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
        Initialize TransferGeneratorService with StarkbankIntegration instance.

        Args:
            - settings_file_path (str): Path to the configuration file.
            - private_key_path (str): Path to the private key file.
        """
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
        Run the transfer generator service using StarkbankIntegration instance.
        """
        try:
            # Connect to Stark Bank API for authentication
            self.engine.connect()

            start_time = time.time()
            end_time = start_time + self.params['duration_time']

            while time.time() < end_time:
                # Listen to webhook events
                events_response = self.engine.listen_webhook_events()
                print(events_response.json())

                # Process webhook events
                self.engine.process_webhook_events(events_response)

                # Wait for the next batch
                time.sleep(self.params['repetition_time'])

        except StarkbankIntegrationError as e:
            # Log any exception that occurs during webhook listening
            service_logger.error(f'Transfer Handler error: {e}')
        finally:
            # Close the logger handler to flush any buffered logs
            for handler in service_logger.handlers:
                handler.close()
                service_logger.removeHandler(handler)

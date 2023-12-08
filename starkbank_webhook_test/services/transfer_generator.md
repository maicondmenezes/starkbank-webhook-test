# Transfer Generator Service

The Transfer Generator Service is responsible for generating and handling transfers using the Stark Bank API. This service listens to webhook events, processes them, and initiates transfers based on the received data.

## Features

- **Microservices Architecture:** Adopts a microservices architecture for modularity and scalability.
- **StarkBank Integration:** Integrates seamlessly with the StarkBank API to facilitate the generation and processing of transfers.
- **Logging:** Implements a logging mechanism to capture execution details, performance metrics, and error logs for effective monitoring.
- **Configuration:** Reads configuration settings from a designated file, including StarkBank credentials and service parameters.
- **Error Handling:** Incorporates robust error-handling mechanisms to gracefully manage exceptions during the transfer generation and processing.

## Getting Started

To set up the Transfer Generator Service, follow these steps:

1. **Configuration File:** Prepare a configuration file (`transfer_generator_setup.json`) containing the required settings for StarkBank integration and service parameters.
2. **Private Key:** Safely store the private key in a dedicated file (`private-key.pem`) to ensure secure access.
3. **Directories:** Confirm the existence of input and output directories to manage files related to the service.

## Usage

Instantiate the `TransferGeneratorService` class with the paths to the configuration file and private key. Run the service using the `run` method:

```python
from starkbank_webhook_test.services.transfer_generator import TransferGeneratorService

# Paths to configuration and private key files
settings_file_path = 'path/to/settings/transfer_generator_setup.json'
private_key_path = 'path/to/private-key.pem'

# Instantiate the service
transfer_service = TransferGeneratorService(settings_file_path, private_key_path)

# Run the service
transfer_service.run()
```

## Logging

The service logs execution details, performance metrics, and errors. Log files are stored in the logs directory, and messages are captured throughout the service's runtime.

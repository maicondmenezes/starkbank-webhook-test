# Invoice Generator Service

The Invoice Generator Service is designed to automate the process of generating invoices using the StarkBank API. This service is part of a larger system and is responsible for creating invoices based on predefined parameters and handling potential errors during the generation process.

## Features

- **Microservices Architecture:** Utilizes a microservices architecture to create a modular and scalable system.
- **StarkBank Integration:** Integrates with the StarkBank API to facilitate the generation of invoices.
- **Logging:** Implements a logging mechanism to record execution, performance, and error logs for better monitoring.
- **Configuration:** Reads configuration settings from a specified file, including private key information and service parameters.
- **Error Handling:** Implements robust error handling to gracefully manage exceptions during the invoice generation process.

## Getting Started

To set up the Invoice Generator Service, follow these steps:

1. **Configuration File:** Prepare a configuration file (`invoices_generator_setup.json`) with the necessary settings for StarkBank integration and service parameters.
2. **Private Key:** Store the private key in a separate file (`private-key.pem`) for secure access.
3. **Directories:** Ensure the existence of input and output directories for managing files related to the service.

## Usage

Instantiate the `InvoiceGeneratorService` class with the paths to the configuration file and private key. Then, run the service using the `run` method:

```python
from starkbank_webhook_test.services.invoice_generator import InvoiceGeneratorService

# Paths to configuration and private key files
settings_file_path = 'path/to/settings/invoices_generator_setup.json'
private_key_path = 'path/to/private-key.pem'

# Instantiate the service
invoice_service = InvoiceGeneratorService(settings_file_path, private_key_path)

# Run the service
invoice_service.run()
```

## Logging

The service logs execution details, performance metrics, and errors. Log files are stored in the logs directory, and messages are captured during the service's runtime.
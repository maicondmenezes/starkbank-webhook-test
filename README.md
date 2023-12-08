# Starkbank Webhook Test

The Starkbank Webhook Test project is a Python-based application that demonstrates the integration with the Stark Bank API. It includes three main services: Invoice Generator Service, Transfer Generator Service, and the Starkbank Integration Documentation. These services leverage the StarkbankIntegration class for communication with the Stark Bank API, providing functionalities for issuing invoices, handling webhook events, and processing transfers.

## Table of Contents

- [Starkbank Webhook Test](#starkbank-webhook-test)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Structure](#project-structure)
  - [Services](#services)
    - [Invoice Generator Service](#invoice-generator-service)
    - [Transfer Generator Service](#transfer-generator-service)
    - [Starkbank Integration Documentation](#starkbank-integration-documentation)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [DevTasks](#devtasks)  

## Introduction

This project demonstrates the integration with the Stark Bank API through three distinct services. The services are designed to automate the processes of generating invoices, handling transfers, and interacting with the Stark Bank API. The project promotes a modular architecture for scalability and maintainability.

## Project Structure

The project is organized into three main services, each encapsulating specific functionalities:

- **Invoice Generator Service**: Automates the generation of invoices based on predefined parameters using the Stark Bank API.

- **Transfer Generator Service**: Handles the generation and processing of transfers through the Stark Bank API, leveraging webhook events.

- **Starkbank Integration Documentation**: Provides detailed documentation for the StarkbankIntegration class, facilitating seamless integration with the Stark Bank API.

## Services

### Invoice Generator Service

The Invoice Generator Service is designed to automate the process of generating invoices using the StarkBank API. It handles configuration settings, private key management, and error handling during the generation process.

- [Invoice Generator Service README](./starkbank_webhook_test/services/invoice_generator.md)

### Transfer Generator Service

The Transfer Generator Service is responsible for generating and handling transfers using the Stark Bank API. It listens to webhook events, processes them, and initiates transfers based on the received data.

- [Transfer Generator Service README](./starkbank_webhook_test/services/transfer_generator.md)

### Starkbank Integration Documentation

The Starkbank Integration Documentation provides detailed information on the StarkbankIntegration class, which serves as a Python interface for integrating with the Stark Bank API.

- [Starkbank Integration Documentation README](./starkbank_webhook_test/starkbank_integration.md)

## Installation

To install the Starkbank Webhook Test project, follow these steps:

1. **Clone the repository**:

  ```bash
  git clone https://github.com/your-username/starkbank-webhook-test.git
  cd starkbank-webhook-test
  ```

2. **Install Dependencies using Poetry**:

Ensure you have [Poetry](https://python-poetry.org/) installed. If not, you can install it using:

```bash
pip install poetry
```

Then, install the project dependencies using Poetry:

```bash
poetry install
```

Poetry will create a virtual environment and install all the required dependencies.

3. **Activate Virtual Environment** :

If Poetry doesn't automatically activate the virtual environment, you can activate it manually:

```bash
poetry shell
```

Activating the virtual environment is optional but recommended.

## Usage

To use the services provided by the Starkbank Webhook Test project, follow the instructions in the respective service READMEs:

- [Invoice Generator Service Usage](./starkbank_webhook_test/services/invoice_generator.md)
- [Transfer Generator Service Usage](./starkbank_webhook_test/services/transfer_generator.md)

Each service may have specific steps or configurations necessary for execution.

## Documentation

Refer to the documentation for more detailed information on each service and the StarkbankIntegration class:

- [Invoice Generator Service Documentation](./starkbank_webhook_test/services/invoice_generator.md)
- [Transfer Generator Service Documentation](./starkbank_webhook_test/services/transfer_generator.md)
- [Starkbank Integration Documentation](./starkbank_webhook_test/starkbank_integration.md)
- [Authenticator](./starkbank_webhook_test/auth/authenticator.md)

Now you have successfully cloned the repository, installed dependencies, and are ready to use the Starkbank Webhook Test project.

## DevTasks

The Starkbank Webhook Test project includes Taskipy scripts, which are defined in the `task.py` file. These scripts automate common development tasks, enhancing productivity and maintaining code quality.

### Available Scripts

- **Linting:**

  - **Script Name:** `lint`
  - **Command:**
  
    ```bash
    task lint
    ```

  - **Description:** This script uses [Black](https://github.com/psf/black) to format the code and [isort](https://pycqa.github.io/isort/) to organize imports. It ensures consistent code style throughout the project.

- **Lint Check:**

  - **Script Name:** `lint-check`
  - **Command:**

    ```bash
    task lint-check
    ```

  - **Description:** This script checks if the code formatting is consistent without making any changes. It provides a diff of the formatting changes that would be applied.

- **Testing:**

  - **Script Name:** `test`
  - **Command:**

    ```bash
    task test
    ```

  - **Description:** This script uses [pytest](https://pytest.org/) to run tests with additional options for verbosity (`-vv`), capturing output (`-s`), and stopping on the first failure (`-x`). It also generates a coverage report for the project.


> **Note**: 
_This guide assumes that users have Git, Python, and Poetry installed on their machines. Make sure to include any additional instructions specific to your project or environment._

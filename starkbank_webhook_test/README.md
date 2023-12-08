# Starkbank Integration Documentation

## Overview

The StarkbankIntegration class provides a Python interface for integrating with the Stark Bank API. This integration facilitates the issuance of random invoices, webhook event handling, and the initiation of transfers based on paid invoices. The class is designed to simplify the process of interacting with the Stark Bank API, handling authentication, and managing webhook events.

## Table of Contents

- [Starkbank Integration Documentation](#starkbank-integration-documentation)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
    - [Initialization](#initialization)
    - [Authentication](#authentication)
  - [Public Methods](#public-methods)
    - [`connect`](#connect)
    - [`issue_random_invoices`](#issue_random_invoices)
    - [`listen_webhook_events`](#listen_webhook_events)
    - [`process_webhook_events`](#process_webhook_events)
  - [Auxiliary Libraries](#auxiliary-libraries)
    - [`Authenticator`](./starkbank_webhook_test/auth/README.md)
  - [Exceptions](#exceptions)
    - [`StarkbankIntegrationError`](#starkbankintegrationerror)

## Getting Started

### Initialization

To get started, create an instance of the StarkbankIntegration class by providing the required parameters:

```python
from starkbank_webhook_test import StarkbankIntegration

integration = StarkbankIntegration(
    environment='sandbox',
    id='your_project_or_organization_id',
    private_key='your_private_key',
    auth_type='project',  # or 'organization'
    webhook_url='your_webhook_url',
)
```

### Authentication

To authenticate with the Stark Bank API, use the connect method:

```python
integration.connect()
```

## Publice Methods

### connect

Connects to the Stark Bank API using the provided authentication details.

```python
def connect(self):
    """
    Connect to Stark Bank API using the authenticator and set the user attribute.

    Raises:
        - StarkbankIntegrationError: If authentication fails.
    """
```

### issue_random_invoices

Generates a random number of invoices at regular intervals based on the provided parameters.

```python
def issue_random_invoices(self, params):
    """
    Generate a random number of invoices within the specified quantity interval,
    with a repetition time interval, and for a total duration.

    Args:
        params (dict): Dictionary containing the parameters.
            Example:
            {
                'quantity_interval': (8, 12),
                'repetition_time': 180,  # in minutes
                'duration_time': 24,  # in hours
            }
    """
```

### listen_webhook_events

Listens to the webhook events and returns the response containing the events.

```python
def listen_webhook_events(self):
    """
    Public method to listen to the webhook events.

    Returns:
        Response: The response containing the webhook events.

    Raises:
        StarkbankIntegrationError: If an error occurs during webhook listening.
    """
```

### process_webhook_events

Processes the webhook events received in the response.

```python
def process_webhook_events(self, events_response):
    """
    Process the webhook events received in the response.

    Args:
        events_response (Response): The response containing the events.

    Raises:
        StarkbankIntegrationError: If an error occurs during event processing.
    """
```

## Auxiliary Libraries

Organizing code into auxiliary libraries is essential for fostering modular and maintainable software development. It enhances code readability, encourages reusability, and simplifies updates to specific functionalities. This practice also facilitates collaboration among developers and contributes to a more structured and scalable codebase.
Custom libraries to.

### Authenticator

For authentication, the Authenticator class is used. Refer to the Authenticator [Documentation](./auth/README.md) for more details.

## Exceptions

### StarkbankIntegrationError

Custom exception for StarkbankIntegration errors.

```python
class StarkbankIntegrationError(Exception):
    """Custom exception for StarkbankIntegration errors."""
    pass
```

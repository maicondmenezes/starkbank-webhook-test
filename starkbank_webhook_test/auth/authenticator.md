# Authenticator Class for Stark Bank API

## Introduction

The `Authenticator` class is designed to facilitate authentication for Stark Bank API requests. It supports both project and organization authentication types, handles authentication-related errors, and includes a method to create new public and private keys.

## Usage

### Initialization

To use the `Authenticator` class, initialize an instance with the required parameters:

```python
from starkbank_webhook_test.auth.authenticator import Authenticator, AuthenticationError

# Set up authentication parameters
environment = 'sandbox'  # 'sandbox' or 'production'
id = 'your_user_id'
private_key = 'your_private_key_content'
auth_type = 'project'  # 'project' or 'organization'

# Initialize Authenticator
authenticator = Authenticator(environment, id, private_key, auth_type)
```

### Authentication

Authenticate and obtain a Stark Bank user:

```python
try:
    user = authenticator.authenticate()
    # Now 'user' holds the authenticated Stark Bank user (starkbank.Project or starkbank.Organization)
except AuthenticationError as e:
    # Handle authentication errors
    print(f"Authentication failed: {e}")
```

### Key Creation

Create new public and private keys:

```python
try:
    destination_path = 'path/to/keys'
    private_key, public_key = Authenticator.create_keys(destination_path)
    # Now 'private_key' and 'public_key' hold the newly created keys
except AuthenticationError as e:
    # Handle key creation errors
    print(f"Key creation failed: {e}")
```

> Note: Ensure to handle errors appropriately in your application.


### Guidelines

- Always keep private keys secure. Do not share them.
- Avoid hard-coding private keys. Prefer saving them as - environment variables or in encrypted databases.
- Validate input parameters and handle errors gracefully.
- Feel free to customize the Authenticator class based on your application's requirements.
import os

import starkbank


class Authenticator:
    """
    A class for authenticating Stark Bank API requests.

    Attributes:
        - environment (str): The environment ('sandbox' or 'production').
        - id (str): The user ID (Project ID or Organization ID).
        - private_key (str): The private key content for ECDSA authentication.
        - auth_type (str): The type of authentication ('project' or 'organization').
    """

    def __init__(
        self, environment: str, id: str, private_key: str, auth_type: str
    ):
        """
        Initialize the Authenticator with the required data for authentication.

        Args:
            - environment (str): The environment ('sandbox' or 'production').
            - id (str): The user ID (Project ID or Organization ID).
            - private_key (str): The private key content for ECDSA authentication.
            - auth_type (str): The type of authentication ('project' or 'organization').
        """
        self.environment = environment.lower()
        self.id = id
        self.private_key = private_key
        self.auth_type = auth_type.lower()

        self._validate_attributes()

    def _validate_attributes(self):
        """
        Validate the environment and auth_type attributes.
        """
        valid_environments = {'sandbox', 'production'}
        valid_auth_types = {'project', 'organization'}

        if self.environment not in valid_environments:
            raise ValueError(
                f"Invalid environment. Use {', '.join(valid_environments)}."
            )

        if self.auth_type not in valid_auth_types:
            raise ValueError(
                f"Invalid authentication type. Use {', '.join(valid_auth_types)}."
            )

    def authenticate(self):
        """
        Authenticate and return a Stark Bank user based on the authentication type.

        Returns:
            starkbank.Project or starkbank.Organization: The authenticated user.
        """
        try:
            if self.auth_type == 'project':
                user = starkbank.Project(
                    environment=self.environment,
                    id=self.id,
                    private_key=self.private_key,
                )
            elif self.auth_type == 'organization':
                user = starkbank.Organization(
                    environment=self.environment,
                    id=self.id,
                    private_key=self.private_key,
                )
            else:
                raise ValueError(
                    "Invalid authentication type. Use 'project' or 'organization'."
                )

            starkbank.user = user
            return user

        except starkbank.error.InvalidSignatureError as e:
            raise AuthenticationError(f'Invalid signature: {e}')

        except starkbank.error.InputErrors as e:
            raise AuthenticationError(f'Input errors: {e}')

        except starkbank.error.InternalServerError as e:
            raise AuthenticationError(f'Internal server error: {e}')

        except Exception as e:
            raise AuthenticationError(f'An unexpected error occurred: {e}')

    @classmethod
    def create_keys(cls, destination_path: str):
        """
        Create new public and private keys in the specified directory.

        Args:
            - destination_path (str): The directory path where the keys will be saved.

        Returns:
            Tuple[str, str]: The newly created private and public keys.

        Raises:
            - AuthenticationError: If an error occurs during key creation.
        """
        try:
            private_key, public_key = starkbank.key.create(destination_path)
            return private_key, public_key

        except starkbank.error.InternalServerError as e:
            raise AuthenticationError(
                f'Internal server error during key creation: {e}'
            )

        except Exception as e:
            raise AuthenticationError(
                f'An unexpected error occurred during key creation: {e}'
            )


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""

    pass

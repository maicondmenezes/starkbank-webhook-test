from urllib.parse import urlparse

from starkbank_webhook_test.auth.authenticator import AuthenticationError, Authenticator


class StarkbankIntegration:
    """
    A class for integrating with Stark Bank API.

    Attributes:
        - authenticator (Authenticator): The Authenticator instance for authentication.
        - user (starkbank.Project or starkbank.Organization): The authenticated Stark Bank user.
        - webhook (Webhook): The Webhook instance for handling callback events.
    """

    def __init__(
        self,
        environment: str,
        id: str,
        private_key: str,
        auth_type: str,
        webhook_url: str,
    ):
        """
        Initialize the StarkbankIntegration with the required data.

        Args:
            - environment (str): The environment ('sandbox' or 'production').
            - id (str): The user ID (Project ID or Organization ID).
            - private_key (str): The private key content for ECDSA authentication.
            - auth_type (str): The type of authentication ('project' or 'organization').
            - webhook_url (str): The URL for the webhook.
        """
        try:
            self.authenticator = Authenticator(
                environment, id, private_key, auth_type
            )
            self._validate_webhook_url(webhook_url)
            self.webhook = webhook_url
        except ValueError as ve:
            raise StarkbankIntegrationError(f'Invalid parameter: {ve}')
        except AuthenticationError as ae:
            raise StarkbankIntegrationError(f'Authentication failed: {ae}')

        self.user = None

    def _validate_webhook_url(self, webhook_url: str):
        """
        Validate that the provided webhook_url is a valid URL.

        Args:
            - webhook_url (str): The URL for the webhook.

        Raises:
            - ValueError: If the URL is not valid.
        """
        parsed_url = urlparse(webhook_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(
                'Invalid webhook_url. Please provide a valid URL.'
            )

    def connect(self):
        """
        Connect to Stark Bank API using the authenticator and set the user attribute.

        Raises:
            - StarkbankIntegrationError: If authentication fails.
        """
        try:
            self.user = self.authenticator.authenticate()
        except AuthenticationError as ae:
            raise StarkbankIntegrationError(f'Authentication failed: {ae}')


class StarkbankIntegrationError(Exception):
    """Custom exception for StarkbankIntegration errors."""

    pass

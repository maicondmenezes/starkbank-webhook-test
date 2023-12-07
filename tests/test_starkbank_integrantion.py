import unittest
from unittest.mock import Mock, patch

from starkbank_webhook_test.auth.authenticator import Authenticator
from starkbank_webhook_test.starkbank_integration import (
    StarkbankIntegration,
    StarkbankIntegrationError,
)


class TestStarkbankIntegration(unittest.TestCase):
    """
    Unit test case for the StarkbankIntegration class.
    """

    def setUp(self):
        """
        Set up common variables for tests.
        """
        self.valid_environment = 'sandbox'
        self.valid_id = '1234567890'
        self.valid_private_key = 'valid_private_key_content'
        self.valid_auth_type = 'project'
        self.valid_webhook_url = 'http://example.com/webhook'

    @patch(
        'starkbank_webhook_test.starkbank_integration.Authenticator',
        autospec=True,
    )
    def test_init_success(self, mock_authenticator):
        """
        Test successful initialization of StarkbankIntegration.
        """
        integration = StarkbankIntegration(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
            webhook_url=self.valid_webhook_url,
        )
        self.assertIsInstance(integration.authenticator, Authenticator)
        self.assertIsNone(integration.user)

    @patch(
        'starkbank_webhook_test.starkbank_integration.Authenticator',
        autospec=True,
        side_effect=StarkbankIntegrationError('Authentication failed'),
    )
    def test_init_authenticator_failure(self, mock_authenticator):
        """
        Test failure during initialization due to authentication error.
        """
        with self.assertRaises(StarkbankIntegrationError) as context:
            StarkbankIntegration(
                environment=self.valid_environment,
                id=self.valid_id,
                private_key=self.valid_private_key,
                auth_type=self.valid_auth_type,
                webhook_url=self.valid_webhook_url,
            )
        self.assertEqual(str(context.exception), 'Authentication failed')

    @patch(
        'starkbank_webhook_test.starkbank_integration.StarkbankIntegration._validate_webhook_url',
        autospec=True,
    )
    @patch(
        'starkbank_webhook_test.starkbank_integration.Authenticator',
        autospec=True,
    )
    def test_init_invalid_webhook_url(
        self, mock_authenticator, mock_validate_url
    ):
        """
        Test failure during initialization due to invalid webhook URL.
        """
        mock_validate_url.side_effect = ValueError('Invalid webhook_url')
        with self.assertRaises(StarkbankIntegrationError) as context:
            StarkbankIntegration(
                environment=self.valid_environment,
                id=self.valid_id,
                private_key=self.valid_private_key,
                auth_type=self.valid_auth_type,
                webhook_url='invalid_url',
            )
        self.assertTrue(
            str(context.exception).startswith(
                'Invalid parameter: Invalid webhook_url'
            )
        )

    @patch(
        'starkbank_webhook_test.starkbank_integration.Authenticator.authenticate',
        autospec=True,
    )
    def test_connect_success(self, mock_authenticate):
        """
        Test successful connection to Stark Bank API.
        """
        integration = StarkbankIntegration(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
            webhook_url=self.valid_webhook_url,
        )

        integration.connect()
        self.assertIsInstance(integration.user, Mock)

    @patch(
        'starkbank_webhook_test.starkbank_integration.Authenticator.authenticate',
        autospec=True,
        side_effect=StarkbankIntegrationError('Authentication failed'),
    )
    def test_connect_failure(self, mock_authenticate):
        """
        Test failure during connection due to authentication error.
        """
        integration = StarkbankIntegration(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
            webhook_url=self.valid_webhook_url,
        )

        with self.assertRaises(StarkbankIntegrationError) as context:
            integration.connect()
        self.assertEqual(str(context.exception), 'Authentication failed')


if __name__ == '__main__':
    unittest.main()
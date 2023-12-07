import unittest
from unittest.mock import Mock, patch

import starkbank

from starkbank_webhook_test.auth.authenticator import AuthenticationError, Authenticator


class TestAuthenticator(unittest.TestCase):
    """
    Unit test case for the Authenticator class.
    """

    def setUp(self):
        """
        Set up common variables for tests.
        """
        self.valid_private_key = """
        -----BEGIN EC PARAMETERS-----
        BgUrgQQACg==
        -----END EC PARAMETERS-----
        -----BEGIN EC PRIVATE KEY-----
        MHQCAQEEIMCwW74H6egQkTiz87WDvLNm7fK/cA+ctA2vg/bbHx3woAcGBSuBBAAK
        oUQDQgAE0iaeEHEgr3oTbCfh8U2L+r7zoaeOX964xaAnND5jATGpD/tHec6Oe9U1
        IF16ZoTVt1FzZ8WkYQ3XomRD4HS13A==
        -----END EC PRIVATE KEY-----
        """
        self.valid_environment = 'sandbox'
        self.valid_id = '1234567890'
        self.valid_auth_type = 'project'

    def test_init_success(self):
        """
        Test successful initialization of Authenticator.
        """
        authenticator = Authenticator(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
        )
        self.assertEqual(
            authenticator.environment, self.valid_environment.lower()
        )
        self.assertEqual(authenticator.id, self.valid_id)
        self.assertEqual(authenticator.private_key, self.valid_private_key)
        self.assertEqual(authenticator.auth_type, self.valid_auth_type.lower())

    def test_authenticate_project_success(self):
        """
        Test successful authentication for a project user.
        """
        expected_user_id = '1234567890'
        authenticator = Authenticator(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
        )
        user = authenticator.authenticate()
        self.assertEqual(expected_user_id, user.id)

    @patch(
        'starkbank.Project',
        side_effect=starkbank.error.InvalidSignatureError(
            [dict(code='99', message='Invalid signature')]
        ),
    )
    def test_authenticate_project_invalid_signature(self, mock_user):
        """
        Test failure due to invalid signature during project authentication.
        """
        authenticator = Authenticator(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
        )
        with self.assertRaises(AuthenticationError) as context:
            authenticator.authenticate()
        self.assertTrue(str(context.exception).startswith('Invalid signature'))

    @patch(
        'starkbank.Project',
        side_effect=starkbank.error.InputErrors(
            [dict(code='99', message='Invalid input')]
        ),
    )
    def test_authenticate_project_invalid_input_errors(self, mock_user):
        """
        Test failure due to invalid input errors during project authentication.
        """
        authenticator = Authenticator(
            environment=self.valid_environment,
            id=self.valid_id,
            private_key=self.valid_private_key,
            auth_type=self.valid_auth_type,
        )
        with self.assertRaises(AuthenticationError) as context:
            authenticator.authenticate()

        self.assertTrue(str(context.exception).startswith('Input errors'))

    @patch(
        'starkbank.key.create',
        return_value=('mocked_private_key', 'mocked_public_key'),
    )
    def test_create_keys_success(self, mock_create):
        """
        Test successful creation of public and private keys.
        """
        destination_path = 'sample/destination/path'
        private_key, public_key = Authenticator.create_keys(destination_path)
        mock_create.assert_called_once_with(destination_path)
        self.assertEqual(private_key, 'mocked_private_key')
        self.assertEqual(public_key, 'mocked_public_key')

    @patch(
        'starkbank.key.create',
        side_effect=starkbank.error.InternalServerError('Server error'),
    )
    def test_create_keys_internal_server_error(self, mock_create):
        """
        Test failure due to internal server error during key creation.
        """
        destination_path = 'sample/destination/path'
        with self.assertRaises(AuthenticationError) as context:
            Authenticator.create_keys(destination_path)
        mock_create.assert_called_once_with(destination_path)
        self.assertEqual(
            str(context.exception),
            'Internal server error during key creation: Server error',
        )


if __name__ == '__main__':
    unittest.main()

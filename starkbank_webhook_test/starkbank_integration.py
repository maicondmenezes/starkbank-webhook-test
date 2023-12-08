import time
from datetime import datetime, timedelta
from random import randint, sample, uniform
from urllib.parse import urlparse

from faker import Faker
from starkbank import Invoice
from starkbank.transfer import Rule

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

    def _parse_params(self, params):
        """
        Parse parameters from the input dictionary.

        Args:
            params (dict): Input parameters.

        Returns:
            Tuple: Tuple containing quantity_interval, repetition_time, and duration_time.
        """
        quantity_interval = params.get('quantity_interval', (8, 12))
        repetition_time = params.get('repetition_time', 180)
        duration_time = params.get('duration_time', 24)
        return quantity_interval, repetition_time, duration_time

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
        quantity_interval, repetition_time, duration_time = self._parse_params(
            params
        )

        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=duration_time)

        while datetime.utcnow() < end_time:
            num_invoices = randint(*quantity_interval)
            self._issue_invoices(num_invoices, repetition_time)
            time.sleep(repetition_time)

    def _issue_invoices(self, num_invoices, repetition_time):
        """
        Issue the specified number of random invoices at regular intervals.

        Args:
            num_invoices (int): Number of invoices to issue.
            repetition_time (int): Repetition time interval in minutes.
        """
        time_interval = repetition_time / num_invoices

        for _ in range(num_invoices):
            self._issue_single_invoice()
            time.sleep(time_interval)

    def _generate_random_invoice_data(
        self,
        amount_range=(1000, 1000000),
        discounts_count_range=(1, 5),
        descriptions_count_range=(1, 15),
        tags_count_range=(0, 8),
        rules_count_range=(0, 4),
    ):
        """
        Generate random data for an invoice.
        """
        try:
            fake = Faker()
            required_fields = ['amount', 'taxId', 'name']
            optional_fields = [
                'due',
                'fine',
                'interest',
                'expiration',
                'discounts',
                'descriptions',
                'tags',
                'rules',
            ]

            data = {
                field: self._generate_required_field(field, fake, amount_range)
                for field in required_fields
            }

            additional_fields = sample(
                optional_fields, k=randint(0, len(optional_fields))
            )
            for field in additional_fields:
                data[field] = self._generate_additional_field(
                    field,
                    fake,
                    discounts_count_range,
                    descriptions_count_range,
                    tags_count_range,
                    rules_count_range,
                )

            return data

        except Exception as e:
            raise StarkbankIntegrationError(
                f'Error generating random invoice data: {e}'
            )

    def _generate_required_field(self, field, fake, amount_range):
        """
        Generate a random value for a specific field.
        """
        if field == 'amount':
            return randint(*amount_range)
        elif field == 'taxId':
            return fake.cpf()
        elif field == 'name':
            return fake.name()

        return None

    def _generate_additional_field(
        self,
        field,
        fake,
        discounts_count_range,
        descriptions_count_range,
        tags_count_range,
        rules_count_range,
    ):
        """
        Generate a random value for an additional field.
        """
        if field == 'due':
            return datetime.utcnow() + timedelta(hours=randint(1, 24))
        elif field == 'fine':
            return round(uniform(0.1, 4.0), 2)
        elif field == 'interest':
            return round(uniform(0.1, 2.0), 2)
        elif field == 'expiration':
            return round(timedelta(hours=randint(1, 72)).total_seconds())
        elif field == 'discounts':
            return self._generate_discounts(fake, discounts_count_range)
        elif field == 'descriptions':
            return self._generate_descriptions(fake, descriptions_count_range)
        elif field == 'tags':
            return [fake.word() for _ in range(randint(*tags_count_range))]
        elif field == 'rules':
            return self._generate_rules(fake, rules_count_range)

        return None

    def _generate_discounts(self, fake, discounts_count_range):
        """
        Generate random discounts data.
        """
        discounts = []
        for _ in range(randint(*discounts_count_range)):
            discount = {
                'percentage': round(uniform(1.0, 20.0), 2),
                'due': datetime.utcnow() + timedelta(hours=randint(1, 72)),
            }
            discounts.append(discount)
        return discounts

    def _generate_descriptions(self, fake, descriptions_count_range):
        """
        Generate random descriptions data.
        """
        descriptions = []
        for _ in range(randint(*descriptions_count_range)):
            description = {
                'key': fake.word(),
                'value': fake.currency_code()
                + str(round(uniform(1.0, 100.0), 2)),
            }
            descriptions.append(description)
        return descriptions

    def _generate_rules(self, fake, rules_count_range):
        """
        Generate random rules data.
        """
        rules = []
        for _ in range(randint(*rules_count_range)):
            rule_key = fake.word()
            rule_value = (
                [fake.cpf() for _ in range(randint(1, 5))]
                if rule_key == 'allowedTaxIds'
                else fake.random_int(1, 10)
            )
            rule = Rule(key=rule_key, value=rule_value)
            rules.append(rule)
        return rules

    def _issue_single_invoice(
        self,
        amount_range=(1000, 50000),
        discounts_count_range=(1, 5),
        descriptions_count_range=(1, 15),
        tags_count_range=(0, 8),
        rules_count_range=(0, 4),
    ):
        """
        Issue a single random invoice.
        """
        try:
            invoice_data = self._generate_random_invoice_data(
                amount_range,
                discounts_count_range,
                descriptions_count_range,
                tags_count_range,
                rules_count_range,
            )

            optional_fields = [
                'due'
                'fine'
                'interest'
                'expiration'
                'discounts'
                'descriptions'
                'tags'
                'rules'
            ]
            optional_data = {
                key: invoice_data.get(key)
                for key in optional_fields
                if invoice_data.get(key)
            }

            return Invoice(
                amount=invoice_data.get('amount'),
                tax_id=invoice_data.get('taxId'),
                name=invoice_data.get('name'),
                **optional_data,
            )
        except Exception as e:
            raise StarkbankIntegrationError(
                f'Error issuing a single random invoice: {e}'
            )


class StarkbankIntegrationError(Exception):
    """Custom exception for StarkbankIntegration errors."""

    pass

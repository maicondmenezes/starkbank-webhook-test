import asyncio
from multiprocessing import Process
from starkbank_webhook_test.constants import PRIVATE_KEY_PATH
from starkbank_webhook_test.services.invoice_generator import (
    SETTINGS_FILE_PATH as INVOICE_GENERATOR_SETTINGS_FILE,
)
from starkbank_webhook_test.services.transfer_generator import (
    SETTINGS_FILE_PATH as TRANSFER_GENERATOR_SETTINGS_FILE,
)
from starkbank_webhook_test.services.transfer_generator import TransferGeneratorService
from starkbank_webhook_test.services.invoice_generator import InvoiceGeneratorService


def invoice_generator():
    invoice_generator_service = InvoiceGeneratorService(
        settings_file_path=INVOICE_GENERATOR_SETTINGS_FILE,
        private_key_path=PRIVATE_KEY_PATH,
    )

    invoice_generator_service.run()


def transfer_generator():
    transfer_generator_service = TransferGeneratorService(
        settings_file_path=TRANSFER_GENERATOR_SETTINGS_FILE,
        private_key_path=PRIVATE_KEY_PATH,
    )

    transfer_generator_service.run()

async def main():
    loop = asyncio.get_event_loop()    
    tasks = [
        loop.run_in_executor(None, invoice_generator),
        loop.run_in_executor(None, transfer_generator),
    ]
    
    await asyncio.gather(*tasks)


if __name__ == "__main__":    
    asyncio.run(main())
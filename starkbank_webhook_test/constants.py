import os

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(SOURCE_DIR + '/../')
INPUT_DIR = os.path.join(ROOT_DIR, 'input')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
PRIVATE_KEY_PATH = os.path.join(INPUT_DIR, 'credentials/private-key.pem')
PUBLIC_KEY_PATH = os.path.join(INPUT_DIR, 'credentials/public-key.pem')

import os
from dotenv import load_dotenv

load_dotenv()

# Amazon Creators API
AMAZON_CREDENTIAL_ID = os.getenv('AMAZON_CREDENTIAL_ID')
AMAZON_CREDENTIAL_SECRET = os.getenv('AMAZON_CREDENTIAL_SECRET')
AMAZON_CREDENTIAL_VERSION = os.getenv('AMAZON_CREDENTIAL_VERSION', '2.1')
AMAZON_PARTNER_TAG = os.getenv('AMAZON_PARTNER_TAG')
AMAZON_MARKETPLACE = os.getenv('AMAZON_MARKETPLACE', 'www.amazon.com.br')

EVOLUTION_API_URL = os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')
EVOLUTION_API_KEY = os.getenv('EVOLUTION_API_KEY')
EVOLUTION_INSTANCE_NAME = os.getenv('EVOLUTION_INSTANCE_NAME')

WHATSAPP_GROUP_ID = os.getenv('WHATSAPP_GROUP_ID')

PRICE_DROP_THRESHOLD = float(os.getenv('PRICE_DROP_THRESHOLD', '10'))
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '60'))
MAX_PRODUCTS_PER_MESSAGE = int(os.getenv('MAX_PRODUCTS_PER_MESSAGE', '5'))

DATABASE_PATH = 'products.db'

TECH_CATEGORIES = [
    'Electronics',
    'Computers',
    'Cell Phones & Accessories',
    'Camera & Photo',
    'Headphones',
    'Video Games',
    'Wearable Technology',
    'Smart Home',
    'PC Gaming',
    'Computer Accessories'
]

SEARCH_KEYWORDS = [
    'smartphone',
    'fone bluetooth',
    'smartwatch',
    'tablet',
    'notebook',
    'mouse gamer',
    'teclado mecânico',
    'webcam',
    'SSD',
    'carregador rápido',
    'power bank',
    'alexa',
    'chromecast',
    'ring light'
]

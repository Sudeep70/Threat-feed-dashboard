import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Database
DATABASE_PATH = 'threats.db'

# Alert thresholds
CRITICAL_CONFIDENCE_THRESHOLD = 80  # Confidence score to trigger alert
MAX_ALERTS_PER_RUN = 5  # Limit alerts per collection run

# Collection settings
MAX_RESULTS_PER_SOURCE = 10  # How many threats to fetch per source

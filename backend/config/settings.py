import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend/.env
project_root = Path(__file__).parent.parent.parent
dotenv_path = project_root / "backend" / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4o')

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Service Configuration
TICKETING_SYSTEM_URL = os.getenv('TICKETING_SYSTEM_URL', 'http://localhost:9000')
DIRECTORY_SERVICE_URL = os.getenv('DIRECTORY_SERVICE_URL', 'http://localhost:9001')

# Application Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Safety & Compliance
MAX_AUTO_EXECUTE_ACTIONS = int(os.getenv('MAX_AUTO_EXECUTE_ACTIONS', '3'))
REQUIRE_APPROVAL_FOR_SENSITIVE = os.getenv('REQUIRE_APPROVAL_FOR_SENSITIVE', 'true').lower() == 'true'

def validate_config():
    """Validate that required configuration is present."""
    missing = []
    
    if not AZURE_OPENAI_ENDPOINT:
        missing.append('AZURE_OPENAI_ENDPOINT')
    if not AZURE_OPENAI_API_KEY:
        missing.append('AZURE_OPENAI_API_KEY')
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Please check your .env file."
        )

# Validate on import (optional - comment out if you want lazy validation)
# validate_config()

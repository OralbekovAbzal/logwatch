import os
from dotenv import load_dotenv
from models import ConfigError

load_dotenv()

try:
    limit_p95 = int(os.getenv("SLO_P95_MS"))
except ValueError:
    raise ConfigError(f"invalid SLO_P95_MS: '{os.getenv("SLO_P95_MS")}'")

try:
    error_rate = float(os.getenv("SLO_ERROR_RATE"))
except ValueError:
    raise ConfigError(f"invalid SLO_ERROR_RATE: '{os.getenv("SLO_ERROR_RATE")}'")
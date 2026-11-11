import os
from dotenv import load_dotenv
from models import ConfigError

load_dotenv()
def load_config() -> tuple[int, float]:
    if os.getenv("SLO_P95_MS") is None:
        limit_p95 = 6000
    else:
        try:
            limit_p95 = int(os.getenv("SLO_P95_MS"))
            if limit_p95 < 1:
                raise ValueError
        except ValueError:
            raise ConfigError(f"invalid SLO_P95_MS: '{os.getenv("SLO_P95_MS")}'")

    if os.getenv("SLO_ERROR_RATE") is None:
        error_rate = 0.2
    else:
        try:
            error_rate = float(os.getenv("SLO_ERROR_RATE"))
            if 0 < error_rate > 1:
                raise ValueError
        except ValueError:
            raise ConfigError(f"invalid SLO_ERROR_RATE: '{os.getenv("SLO_ERROR_RATE")}'")

    return limit_p95, error_rate

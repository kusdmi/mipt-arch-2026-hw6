import requests
import logging
import time
from currency_converter import RateProvider


class ApiRateProvider(RateProvider):
    """Fetches exchange rates from API with retry support."""

    def __init__(
        self,
        api_url: str = "https://api.exchangerate-api.com/v4/latest/USD",
        max_retries: int = 3,
        retry_delay: int = 2,
    ):
        self.api_url = api_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("RateProvider")

        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def get_rates(self) -> dict:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.api_url, timeout=10)
                response.raise_for_status()

                data = response.json()
                return data["rates"]

            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"Request failed ({attempt + 1}/{self.max_retries}): {e}"
                )

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        raise RuntimeError("Failed to fetch exchange rates")
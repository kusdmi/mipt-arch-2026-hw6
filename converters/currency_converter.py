from abc import ABC, abstractmethod


class RateProvider(ABC):
    """Interface for obtaining currency rates."""

    @abstractmethod
    def get_rates(self) -> dict:
        pass


class CurrencyConverter:
    """Converts USD to other currencies using provided rates."""

    def __init__(self, rate_provider: RateProvider):
        self._rate_provider = rate_provider
        self._rates = self._rate_provider.get_rates()

        if not self._rates:
            raise RuntimeError("Unable to load exchange rates")

    def convert(self, amount: float, target_currency: str) -> float:
        if target_currency not in self._rates:
            raise ValueError(f"Currency {target_currency} not supported")

        return amount * self._rates[target_currency]
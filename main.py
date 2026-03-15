from currency_converter import CurrencyConverter
from api_rate_provider import ApiRateProvider


def main():
    amount = float(input("Введите значение в USD:\n"))

    provider = ApiRateProvider()
    converter = CurrencyConverter(provider)

    currencies = ["RUB", "EUR", "GBP", "CNY"]

    for currency in currencies:
        result = converter.convert(amount, currency)
        print(f"{amount} USD to {currency}: {result:.2f}")


if __name__ == "__main__":
    main()
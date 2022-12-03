from requests import get
from pprint import PrettyPrinter
import json
from decouple import config

BASE_URL = config("BASE_URL")
API_KEY = config("API_KEY")

# prints data in a more human-readable format
printer = PrettyPrinter()


# define a function to get currencies from api
def get_currencies():
    # assign a variable for the endpoint
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    # assign a variable for the complete url
    url = BASE_URL + endpoint
    # assign a variable to get data from the json object
    data = get(url).json()["results"]

    # make data a list instead of a dictionary to sort the data
    data = list(data.items())

    # sort the data
    data.sort()

    return data


# create a function to print the formatted currency
def print_currencies(currencies):
    for name, currency in currencies:
        name = currency["currencyName"]
        _id = currency["id"]
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")


# define a function to get the exchange rates for a currency
def exchange_rate(currency1, currency2):
    endpoint = (
        f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    )
    url = BASE_URL + endpoint
    data = get(url).json()

    if len(data) == 0:
        print("Invalid currencies.")
        return

    rate = list(data.values())[0]
    print(f"{currency1} -> {currency2} = {rate}")

    return rate


def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return
    try:
        amount = float(amount)
    except:
        print("Invalid amount.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
    return converted_amount


def main():
    currencies = get_currencies()

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1} ")
            currency2 = input("Enter a currency to convert to: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")


main()

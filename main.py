# Used to access CryptoCompare REST API
import requests
# Used to work with json files
import json

# URL for the CryptoCompare REST API
api_url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,ETC&tsyms=USD'


# starting point for the program
def main():
    user = Users()
    user.currencies['USD'] = 1000000
    buy(user, 'BTC', 2)
    print(user.currencies)


# Get a list of crypto currency values from the CryptoCompare API
def get_list():
    resp = requests.get(api_url)
    return json.loads(resp.content)


# function to purchase cryprocurrency with USD
def buy(user, currency, quantity):
    rates = get_list()
    try:
        price = rates[currency]['USD'] * quantity
    except KeyError:
        return False

    if user.currencies['USD'] >= price:
        user.currencies['USD'] -= price
        user.currencies[currency] += quantity

    return


# function to sell cryptocurrency for USD
def sell(user, currency, quantity):
    rates = get_list()
    try:
        price = rates[currency]['USD'] * quantity
    except KeyError:
        return False

    if user.currencies[currency] >= quantity:
        user.currencies[currency] -= quantity
        user.currencies['USD'] += price

    return


# User class holds user info
class Users:
    currencies = {'USD': 0, 'BTC': 0, 'ETH': 0, 'ETC': 0}


if __name__ == "__main__":
    main()

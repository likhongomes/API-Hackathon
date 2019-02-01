# Used to access CryptoCompare REST API
import requests
# Used to work with json files
import json
# URL for the CryptoCompare REST API
api_url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,ETC&tsyms=USD'


# starting point for the program
def main():
    user = Users()
    buy(user)


# Get a list of crypto currency values from the CryptoCompare API
def get_list():
    resp = requests.get(api_url)
    return resp.content


# function to purchase cryprocurrency with USD
def buy(user):
    return


# function to sell cryptocurrency for USD
def sell(user):
    return


# User class holds user info
class Users:
    money = 0
    btc = 0
    eth = 0
    etc = 0


if __name__ == "__main__":
    main()

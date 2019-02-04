# Used to access CryptoCompare REST API
import requests
# Used for interacting with Slack's bot API
from slackclient import SlackClient
# Used to work with json files
import json

import time

# Constants
READ_DELAY = 1  # 1 second  between reading from RTM
BUY_CMD = "buy"  # trigger for buy command
SELL_CMD = "sell"  # trigger for sell command
SHOW_CMD = "whoami"  # trigger for show stats command
CURRENCY_LIST = ["BTC", "ETH", "ETC"]  # list of available currencies
START_MONEY = 10000.00
# URL for the CryptoCompare REST API
API_URL = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=USD,BTC,ETH,ETC&tsyms=USD,BTC,ETH,ETC'

user_list = []


# Parses the events pulled from slack, and returns messages sent to the bot
def parse_command(slack_events):
    # search all new events
    for event in slack_events:
        # get all new messages
        if event["type"] == "message" and not "subtype" in event:
            # get user
            user = get_user(event["user"])
            handle_command(event["text"], event["channel"], user)
    else:
        return None, None


# Handles all slack commands
def handle_command(command, channel, user):
    # split up command into a list
    cmd_list = command.split(" ")
    # if buy command
    if command.startswith(BUY_CMD):
        # if incorrect number of arguments
        if len(cmd_list) != 3:
            # response is an error
            response = "Error, command in the wrong format"
        # if using an invalid currency
        elif cmd_list[1].upper() not in CURRENCY_LIST:
            # response is an error
            response = "Error, invalid currency"
        # if provided qty is not an int
        elif not is_int(cmd_list[2]):
            response = "Error: please enter a valid integer"
        # else everything is good
        else:
            response = buy(user, cmd_list[1].upper(), int(cmd_list[2]))
    # if sell command
    elif command.startswith(SELL_CMD):
        # if incorrect number of arguments
        if len(cmd_list) != 3:
            # response is an error
            response = "Error, command in the wrong format"
        # if using an invalid currency
        elif cmd_list[1].upper() not in CURRENCY_LIST:
            # response is an error
            response = "Error, invalid currency"
        # if provided qty is not an int
        elif not is_int(cmd_list[2]):
            response = "Error: please enter a valid integer"
        # else everything is good
        else:
            response = sell(user, cmd_list[1].upper(), int(cmd_list[2]))

    # else show command
    elif command.startswith(SHOW_CMD):
        if len(cmd_list) != 1:
            response = "Error, command in the wrong format"
        else:
            response = show_user(user)
    # else command not recognised
    else:
        response = "Command not recognised."

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )


# Get a list of crypto currency values from the CryptoCompare API
def get_list():
    resp = requests.get(API_URL)
    return json.loads(resp.content)


# function to exchange two currencies
def transaction(user, fromCurrency, toCurrency, quantity):
    rates = get_list()
    try:
        price = rates[fromCurrency][toCurrency] * quantity
    except KeyError:
        return False

    if int(user.currencies[fromCurrency]) >= price:
        user.currencies[fromCurrency] -= price
        user.currencies[toCurrency] += quantity
        return "Transaction Success: Bought " + str(quantity) + " " + str(toCurrency) + " for " + str(
            price) + fromCurrency
    else:
        return "Transaction Failed: Not enough money"


# function to purchase cryprocurrency with USD
def buy(user, currency, quantity):
    return transaction(user, 'USD', currency, quantity)


# function to sell cryptocurrency for USD
def sell(user, currency, quantity):
    return transaction(user, currency, 'USD', quantity)


def show_user(user):
    response = ("Your stats:\nMoney: " + str(user.currencies['USD']) + "\nBitcoin: " + str(
        user.currencies['BTC']) + "\nEthereum: " + str(user.currencies['ETH']) + "\n Ethereum Classic: " + str(
        user.currencies['ETC']))
    return response


# User class holds user info
class Users:
    currencies = {'ID': "", 'USD': 0.0, 'BTC': 0, 'ETH': 0, 'ETC': 0}


# detects if string is an int
def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# get user object, or create a new one if not found
def get_user(user_id):
    # find user in user list
    for user in user_list:
        if user.currencies['ID'] == user_id:
            return user

    # else no user found
    user = Users()
    user.currencies['ID'] = user_id
    user.currencies['USD'] = START_MONEY
    user_list.append(user)

    return user


if __name__ == "__main__":
    # sign in with API key
    slack_client = SlackClient("xoxb-537411523905-542677057095-l51RA4E44X8n2mokdBnPo8QS")
    # if connected
    if slack_client.rtm_connect(with_team_state=False):
        print("Successfully connected, listening for events")
        while True:
            # get new events
            command, channel = parse_command(slack_client.rtm_read())
            # if new event occurred
            if command:
                print(command)
            time.sleep(READ_DELAY)
    # else could not connect
    else:
        print("Connection Failed")

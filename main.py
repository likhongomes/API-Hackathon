# Used to access CryptoCompare REST API
import requests
# Used for interacting with Slack's bot API
from slackclient import SlackClient
# Used to work with json files
import time

# Constants
READ_DELAY = 1 # 1 second  between reading from RTM
BUY_CMD = "buy" # trigger for buy command
SELL_CMD = "sell" # trigger for sell command
SHOW_CMD = "whoami" # trigger for show stats command
# URL for the CryptoCompare REST API
API_URL = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,ETC&tsyms=USD'


# Parses the events pulled from slack, and returns messages sent to the bot
def parse_command(slack_events):
    # search all new events
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            handle_command(event["text"], event["channel"], event["user"])
    else:
        return None, None


# Handles all slack commands
def handle_command(command, channel, user):
    # default response in case of errors
    default_response = "Error, please tyt the buy, sell, or whoami command"

    # split up command into a list
    cmd_list = command.split(" ")

    # if buy command
    if command.startswith(BUY_CMD):
        if len(cmd_list) != 3:
            response = "Error, command in the wrong format"
    # if sell command
    elif command.startswith(SELL_CMD):
        if len(cmd_list) != 3:
            response = "Error, command in the wrong format"
    # else show command
    elif command.startswith(SHOW_CMD):
        if len(cmd_list) != 1:
            response = "Error, command in the wrong format"
    # else command not recognised
    else:
        response = "Command not recognised."

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


# Get a list of crypto currency values from the CryptoCompare API
def get_list():
    resp = requests.get(API_URL)
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
    # sign in with API key
    slack_client = SlackClient("xoxb-540913915652-540968828227-3eScQTGsNGIVjTCtMd6tqgYo")
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

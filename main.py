import requests


api_url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,ETC&tsyms=USD'


def main():
    print(get_list())


def get_list():
    resp = requests.get(api_url)
    print(resp.content)
    return resp.content


def buy():
    return


def sell():
    return


if __name__ == "__main__":
    main()


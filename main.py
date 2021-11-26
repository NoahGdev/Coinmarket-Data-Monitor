from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

def main():
    with open('logs.txt', 'r') as f:
            myNames = [line.strip() for line in f]

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
      'slug':'hector-dao',
      'convert':'GBP'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'your_api_key',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)

      price = str(data['data']['13881']['quote']['GBP']['price'])[:9]
      tokenAddy = data['data']['13881']['platform']['token_address']
      onedayChange = data['data']['13881']['quote']['GBP']['percent_change_24h']
      oneHourChange = data['data']['13881']['quote']['GBP']['percent_change_1h']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      time.sleep(100)

    with open('logs.txt') as f:
        r = f.read().splitlines()

    if price == r[-1]:
        #print('Price is still same...')
        pass
    else:
        print('New Price Found')
        with open('logs.txt', 'r+') as f:
            r = f.read().splitlines()
            f.write(f'{price}\n')
        webhook = DiscordWebhook(
        url= 'https://discord.com/api/webhooks/913623876855005184/0QrJLPOJeb95fhnJh2yO9IeVZpD1qC9E--KF0a-gbsXSyFj18aOeIEseEyNJXNPbApgc',
        username="Crypto Monitor",
        content="New Price Detected",
        )

        embed = DiscordEmbed(
        title= 'Hector DAO',
        url = 'https://hectordao.com/',
        description= '', color='43d4a7',
        )

        embed.set_thumbnail(
        url= 'https://cdn.discordapp.com/attachments/913620555498942474/913622329123278938/hec.png')

        embed.add_embed_field(name='Coinmarket',value='https://coinmarketcap.com/currencies/hector-dao/', inline=True)
        embed.add_embed_field(name='Current Price (GBP)',value= str(price), inline=False)
        embed.add_embed_field(name='24h Change %',value= str(onedayChange), inline=True)
        embed.add_embed_field(name='1h Change %',value= str(oneHourChange), inline=True)
        embed.add_embed_field(name='Token Address',value= str(tokenAddy), inline=False)

        embed.set_footer(text="Crypto Monitor", icon_url="https://cdn.discordapp.com/attachments/913620555498942474/913622329123278938/hec.png")
        webhook.add_embed(embed)
        response = webhook.execute()
        print('sent')


if __name__ == "__main__":
    main()
    time.sleep(600)
    print('Slept 10 minutes')

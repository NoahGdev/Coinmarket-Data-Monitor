import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

def main():
    
    with open('logs.txt', 'r+') as f:
        r = f.read().splitlines()
            
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
      'slug':'hector-dao', ## Find any slug in docs
      'convert':'GBP'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'your_api_key',
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
        
      ## The details may be different and you will have to manipulate the json differently
      price = str(data['data']['13881']['quote']['GBP']['price'])[:9]
      tokenAddy = data['data']['13881']['platform']['token_address']
      onedayChange = data['data']['13881']['quote']['GBP']['percent_change_24h']
      oneHourChange = data['data']['13881']['quote']['GBP']['percent_change_1h']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      time.sleep(100)
        
    with open('logs.txt', 'r+') as f:
        r = f.read().splitlines()

    if price == r[-1]:
        #print('Price is still same...')
        pass
    else:
        print('New Price Found')
        # Adds the price to the logs so that it wont send webhook again if it the same price
        with open('logs.txt', 'r+') as f:
            r = f.read().splitlines()
            f.write(f'{price}\n')
            
        webhook = DiscordWebhook(
        url= 'your webhook',
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
    time.sleep(600) ## You can change this to however long you want
    print('Slept 10 minutes')

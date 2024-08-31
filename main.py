import discord
import requests
from bs4 import BeautifulSoup
from discord import SyncWebhook
from discord import Embed
from datetime import datetime

#The ThiBot
def commands():
    async def discordMessage(embed):
        # Personal server Web Hook URL
        #https://discord.com/api/webhooks/1274219134137274451/D3nqVhEZGSH8w48YaMa4wjgvP-HkdYn_ZMBwzS_duZ7nGgCVVzvce8TBdOapYQrLEugF
        # Family server Web Hook URL
        #https://discord.com/api/webhooks/1274223209025241190/QOZeOMgEGMFtIOXkzWiNBKlzwrKjcZ-mwq3_ehoB3yjnmvzyAkf7G0VOgrF-oKuYpfMF
        webhook = SyncWebhook.partial('1274219134137274451', 'D3nqVhEZGSH8w48YaMa4wjgvP-HkdYn_ZMBwzS_duZ7nGgCVVzvce8TBdOapYQrLEugF')
        webhook.send(username ='DiscountBot', embed = embed)
   
    async def discountCheck(message):
            url = message
            html = requests.get(url)
            s = BeautifulSoup(html.text,'html.parser')
            title = s.find('div', class_='apphub_AppName')
            try: 
               original_price = s.find('div', class_='discount_original_price')
               discount_price = s.find('div', class_='discount_final_price')
               percentage_off = s.find('div', class_='discount_pct')
               em = Embed(title = title.text, color = 242424)
               em.add_field(name = 'URL', value = url)
               em.add_field(name = 'Discounted Price', value = discount_price.text)
               em.add_field(name = 'Percentage Off', value = percentage_off.text)
               em.add_field(name = 'Original Price', value = original_price.text)
               em.timestamp = datetime.now()
               em.set_footer(text = 'Powered by ThiBot')
               await message.channel.send('Sale found for ' + title.text + '!')
               await discordMessage(embed = em)
            except:
                price = s.find('div', class_='game_purchase_price price')
                await message.channel.send(title.text + ' is not on sale.')
    
    intents = discord.Intents.default() 
    intents.message_content = True
    client = discord.Client(intents = intents)
    
    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
    
    @client.event
    
    async def on_message(message):
        
        if message.author == client.user:
            return
        if message.author.name == 'nugget8268' or message.author.name == 'mai_0' or message.content.lower().startswith('erm'):
            emoji = '\N{NERD FACE}'
            await message.add_reaction(emoji)
        if message.author.name == 'teal_lol':
            pass
        if message.content.lower().startswith('hello'):
            await message.channel.send('Hello everybody!!!')
        if message.content.startswith('!sender'):
            await message.channel.send(message.author)
        if message.content.startswith('!wishlist https://store.steampowered'):
            f = open('wishlist.txt', 'a')
            g = open('wishlist.txt', 'r+')
            f.write(message.content.replace('!wishlist', '').strip())
            f.write('\n')
            await message.channel.send('Game added to wishlist')
           
            seen = set()
            duplicate = False 
            for line in g:
                game = line.lower()
                if game in seen:
                    duplicate = game
                else:
                    seen.add(line)
            f.close()
        if message.content.startswith('!viewwishlist'):
            f = open("wishlist.txt", "r")
            length = len(open("wishlist.txt", "r").readlines())

            for link in range(length):
                url = f.readline().replace("[", "")
                await message.channel.send(url)
                
        if message.content.startswith('!sales'):
            f = open("wishlist.txt", "r")
            length = len(open("wishlist.txt", "r").readlines())

            for link in range(length):

                url = f.readline().replace("[", "")
                html = requests.get(url)
                s = BeautifulSoup(html.content, 'html.parser')
                title = s.find(class_= "apphub_AppName")
                prettyTitle = title.text
                
                try:        
                    original_price = s.find(class_ = "discount_original_price")
                    discount_price = s.find(class_ = "discount_final_price")
                    percentage_off = s.find(class_ = "discount_pct")

                    em = Embed(title = prettyTitle, color = 242424)
                    em.add_field(name = 'URL', value = url)
                    em.add_field(name = 'Discounted Price', value = discount_price.text)
                    em.add_field(name = 'Percentage Off', value = percentage_off.text)
                    em.add_field(name = 'Original Price', value = original_price.text)
                    em.timestamp = datetime.now()
                    em.set_footer(text = 'Powered by ThiBot')
                    await discordMessage(em)

                except:
                    s.find(class_ = "game_purchase_price price")
                    print(title.text, "is not on Sale")
                
                
            

    client.run('MTI3NDIzMzQyNTU0ODgwNDE0OA.G7JP-J.IZl_1ZwVDyjRwXqH-OV0wISsCqVs73DOnCgOMY')


def main():
    commands()
    

if __name__ == '__main__':
    main()

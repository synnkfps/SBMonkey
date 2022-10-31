import os
import discord
import requests

client = discord.Client(intents=discord.Intents.all())

bz_url = 'https://api.hypixel.net/skyblock/bazaar'
items_url = 'https://api.hypixel.net/resources/skyblock/items'

async def to_shortned(s: str) -> str:
    # 13,526.03
    num = float(s.replace(',','')) #13526.03 (float)
    size = len(str(num).split('.')[0])
    raw = int(str(num).split('.')[0])
    parted = f'{raw:,}'.split('.')[0].split(',')

    print(f'Parted: {parted}\nSize: {size}\nRaw: {raw}\nNum: {num}')

    if size <= 3 and size > 0:
        return f'{parted[0]} coins'
    if size > 3 and size < 7:
        return f'{parted[0]},{parted[1][0]}k'
    if size >= 7 and size < 10:#1700000
        return f'{parted[0]},{parted[1][0]}m'

async def find_item_name_by_id(id):
    r = requests.get(items_url)
    items = r.json()
    for i in items['items']:
        if i['id'] == id:
            return i['name']
            
async def send_msg(msg):
    await client.get_channel(1036693990063472710).send(msg)

async def fetch_gems():
    r = requests.get(bz_url)
    products = r.json()
    if products['success'] == True:
        await send_msg(f'Fetch complete!')
    products = products['products']
    for i in products:
        if i.endswith('_GEM'):
            await send_msg(f'Found \:{i}:\n\tName: {await find_item_name_by_id(i)}\n\tSell Price: {await to_shortned("{:,.2}".format(products[i]["quick_status"]["sellPrice"]))}\n\tBuy Price: {products[i]["quick_status"]["buyPrice"]:,.2f}')
    else:
        await send_msg(f'Finished fetching.')

commands = {
    "gemstones": fetch_gems()
}

@client.event
async def on_ready():
    print(f'{client.user} connected.')

@client.event 
async def on_message(msg):
    if msg.channel.id != 1036693990063472710:
        return 

    if msg.content.startswith('emojis'):
        await send_msg(f'{msg.guild.emojis}')
        if not msg.guild.emojis:
            for i in os.listdir(r'C:\Users\User\Downloads\gemstones'):
                with open(rf'C:\Users\User\Downloads\gemstones\{i}', 'rb') as emoji:
                    await msg.guild.create_custom_emoji(name=i.replace('.PNG', ''), image=emoji.read())

    if msg.content.startswith('help'):
        available = ''''''
        for i in commands:
            available+=f'`{i}`' 
        else:
            await send_msg(f'All the commands available:\n{available}')
    
    if msg.content == 'gemstones debug':
        await commands['gemstones']

    if msg.content.startswith('say'):
        await send_msg(msg.content.split('say')[1].strip())
    if msg.content == 'gemstones profit':
        pass

client.run('')

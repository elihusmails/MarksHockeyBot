import discord
import config

from brains import Brains

client = discord.Client()
brains = Brains()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if message.content.startswith('$hello'):
    #     #await message.channel.send_message('Hello!')
    #     await client.send_message(message. channel, 'Hello!')

    if message.content =='$hello':
        await client.send_message(message. channel, 'Hello')
    elif message.content == '$help':
        await client.send_message(message. channel, brains.processHelp())
    else:
        await client.send_message(message. channel, 'Unknown command\n' + brains.processHelp())

    # brainResponse = brains.process(message.content)
    # await client.send_message(message. channel, brainResponse)

client.run(config.BOT_CONFIG['botToken'])
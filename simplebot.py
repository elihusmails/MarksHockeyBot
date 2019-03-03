import discord
import config

from brains import Brains
import hockeystats

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
    type(message.content)
    if message.content =='$hello':
        await client.send_message(message.channel, 'Hello')
    elif message.content == '$help':
        await client.send_message(message.channel, brains.processHelp())
    elif message.content == '$status':
        await client.send_message(message.channel, brains.getStatus())
    elif message.content == '$scoring.top':
        await client.send_message(message.channel, brains.getTopScorers())
    elif message.content == '$standings':
        await client.send_message(message.channel, brains.getStandings())
    elif message.content == '$games':
        await client.send_message(message.channel, brains.getTodaysGames())
    elif message.content == '$scores':
        await client.send_message(message.channel, hockeystats.currentGameScores())
    elif message.content.startswith('$team.stats'):
        await client.send_message(message.channel, hockeystats.teamStats(message.content))
    elif message.content.startswith('$team.prev'):
        await client.send_message(message.channel, hockeystats.pGame(message.content))
    elif message.content.startswith('$team.next'):
        await client.send_message(message.channel, hockeystats.nGame(message.content))
    else:
        await client.send_message(message.channel, 'Unknown command\n' + brains.processHelp())

client.run(config.BOT_CONFIG['botToken'])
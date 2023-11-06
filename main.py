import discord
from discord.ext import commands
import yt_dlp
import asyncio
from webserver import keep_alive
import os

# Define the bot command prefix and create the bot instance
bot_prefix = '!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Dictionary to store voice clients
voice_clients = {}

# Configure yt-dlp options
yt_opts = {
    'format': 'bestaudio/best',
}
ytdl = yt_dlp.YoutubeDL(yt_opts)

ffmpeg_options = {
    'options': '-vn',
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play')
async def play(ctx, url):
    try:
        if ctx.author.voice and ctx.author.voice.channel:
            if ctx.guild.id in voice_clients:
                await voice_clients[ctx.guild.id].disconnect()  # Disconnect before playing a new song

            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client

        loop = asyncio.get_event_loop()
        info = ytdl.extract_info(url, download=False)

        if 'entries' in info:
            song = info['entries'][0]['url']
        else:
            song = info['url']

        player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
        voice_clients[ctx.guild.id].play(player)

    except Exception as error:
        print(error)

@bot.command(name='pause')
async def pause(ctx):
    try:
        if ctx.guild.id in voice_clients:
            voice_clients[ctx.guild.id].pause()
    except Exception as error:
        print(error)

@bot.command(name='resume')
async def resume(ctx):
    try:
        if ctx.guild.id in voice_clients:
            voice_clients[ctx.guild.id].resume()
    except Exception as error:
        print(error)

@bot.command(name='join')
async def join(ctx):
    try:
        if ctx.author.voice and ctx.author.voice.channel:
            if ctx.guild.id in voice_clients:
                await voice_clients[ctx.guild.id].disconnect()  # Disconnect before joining a new voice channel

            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client
        else:
            await ctx.send('You must be in a voice channel to use this command.')
    except Exception as error:
        print(error)

@bot.command(name='disconnect')
async def disconnect(ctx):
    try:
        if ctx.guild.id in voice_clients:
            await voice_clients[ctx.guild.id].disconnect()
            voice_clients.pop(ctx.guild.id)  # Remove the voice client from the dictionary
        else:
            await ctx.send('Not connected to a voice channel.')
    except Exception as error:
        print(error)

# Keep the bot running
keep_alive()

# Retrieve your bot token from environment variables
TOKEN = os.environ.get('DISCORD_BOT_SECRET')

# Start the bot
bot.run(TOKEN)

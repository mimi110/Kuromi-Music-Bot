
import discord
from discord.ext import commands
import youtube_dl
import asyncio
from webserver import keep_alive
import os




client = commands.Bot(command_prefix='!',intents=discord.Intents.all())




voice_clients = {}

yt_dl_opts = {
  'format': 'bestaudio/best'
}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

#block_words = ["curse_word_1", "curse_word_2", "http://", "https://"]





@client.event

async def on_message(msg):

  
    if msg.content.startswith("!play"):

        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("Error1")

        try:
            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)

        except Exception as Error2:
            print(Error2)


    if msg.content.startswith("!pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as Error2:
            print(Error2)

    if msg.content.startswith("!resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as Error2:
            print(Error2)
  
    if msg.content.startswith("!join"):
        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("Error3")
  
    if msg.content.startswith("!disconnect"):
        try:
            voice_clients[msg.guild.id].disconnect()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as Error2:
            print(Error2)

    if msg.content.startswith("!stop"):
        try:
            voice_clients[msg.guild.id].stop()
        except Exception as Error2:
            print(Error2)


          
          
keep_alive()

TOKEN = os.environ.get("DISCORD_BOT_SECRET")

client.run(TOKEN)
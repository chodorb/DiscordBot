import discord
import youtube_dl
import os
import requests
import random
from discord.ext import commands
from discord.utils import get
Token ="DISCORD TOKEN"
client= commands.Bot(command_prefix = '.')

players = {}

@client.event
async def on_ready():
    print("Bot is read")

@client.command(pass_context=True)    
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"+1")
    
@client.command(pass_context=True)
async def disconnect(ctx):

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"I got kicked out of {channel} :(")
        await ctx.send(f"I got kicked out of {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("I can't leave a channel i'm not on.")

@client.command(pass_context=True)
async def play(ctx, url: str):


    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("old file deleted")
    except PermissionError:
        print("Music already plays")
        await ctx.send("Music alread plays")
        return

    await ctx.send("gimme a second")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Music Ended"))
    
    nname = name.rsplit("-", 2)
    await ctx.send(f"We play: {nname[0]}")
    print("playing\n")

@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_playing():
        print("music paused")
        voice.stop()
        await ctx.send("music paused")
    else:
        print("Music not paused, error")
        await ctx.send("could not pause music ")

@client.command(pass_context=True)
async def start(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()

 
client.run(Token)

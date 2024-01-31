import sys
sys.path.insert(0, 'discord.py-self')
import discord
import aiohttp
import asyncio
import json
import re
import tracemalloc
import os
import string
import io
import requests
import queue
import httpx
import requests
import humanize
import traceback
import random
import time
from discord.ext import commands
from datetime import datetime
from datetime import datetime, timedelta
from datetime import datetime
from datetime import datetime, timezone
from pyfiglet import Figlet



with open('config/config.json') as f:
    config = json.load(f)
    token = config['token']
    prefix = config['prefix'] 
bot = commands.Bot(command_prefix=prefix, self_bot=True)
bot.remove_command('help')

def mainHeader():
    with open('config/config.json') as f:
        config = json.load(f)
        token = config['token']
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    return headers
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def dmall(ctx, *, message):
    for guild in bot.guilds:
        for member in guild.members:
            if member != bot.user:  # Avoid sending messages to the bot itself
                try:
                    await member.send(message)
                    print(f"messaged: {member.name}")
                except:
                    print(f"couldnt message: {member.name}")

        
        



bot.run(token)
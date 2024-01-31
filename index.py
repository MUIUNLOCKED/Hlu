# Modules & Variables
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
from discord.utils import async_all
from datetime import datetime
from datetime import datetime, timedelta
from datetime import datetime
from datetime import datetime, timezone
from pyfiglet import Figlet

tracemalloc.start() 
statuses = []
current_status = 0
afk_users = {}
afk_reason = None
status_changing = False
spamming = False
spam_task = None
q = queue.Queue()

# Bot Config

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

# BOT EVENTS

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Check if the message is sent by the bot itself
        reactions = {
            'hii': '👋',
            'happy': '😄',
            'sad': '😢',
            'fix': '🛠️',
            'bruh': '🗿',
            'oof': '🙃',
            'listen': '👂',
            'nvm': '☝️',
            'sahi': '👌',
            'hmm': '🤔',
            'let me check': '✔️',
            'welcome': '🙏',
            'wlc': '🙏',
            'fool': '🤪',
            'nice' : '✨',
            'cool' : '😎',
            'great' : '✨',
            'wait' : '⌛',
            'wtf' : '🖕',
            'ik' : '️☝️',
            'i know' : '☝️',
            'win it' : '🎉',
            'fuck off' : '🖕',
            'nice': '✨',
            'good': '👍',
            'great': '👌',
            'awesome': '🤩',
            'amazing': '👏',
            'excellent': '👌',
            'fantastic': '🌟',
            'superb': '👌',
            'wonderful': '👏',
            'brilliant': '👍',
            'impressive': '👏',
            'outstanding': '🌟',
            'phenomenal': '👌',
            'splendid': '🌟',
            'terrific': '👍',
            'top-notch': '👏',
            'stellar': '⭐',
            'flawless': '👌',
            'exceptional': '🌟',
            'remarkable': '👏',
            'super': '👍',
            'first-rate': '👌',
            'incredible': '👏',
            'marvelous': '🌟',
            'perfect': '💯',
            'no': '❌',
            'nah': '❌',
            'not': '❌',
            'never': '❌',
            'negative': '❌',
            'don\'t': '❌',
            'do not': '❌',
            'cannot': '❌',
            'can\'t': '❌',
            'won\'t': '❌',
            'refuse': '❌',
            'decline': '❌',
            'reject': '❌',
            'denied': '❌',
            'negative': '❌',
            'thanks': '🙏',
            'thank you': '🙏',
            'thx': '🙏',
            'ty': '🙏',
            'appreciate': '🙏',
            'grateful': '🙏',
            'thankful': '🙏',
            'cheers': '🙏',
            'much obliged': '🙏',
            'many thanks': '🙏',
            'thanks a lot': '🙏',
            'thank you very much': '🙏',
            'thank you so much': '🙏',
            'welcome': '🙏',
            'wlc': '🙏',
            'welc': '🙏',
            'hi': '👋',
            'hello': '👋',
            'hey': '👋',
            'greetings': '👋',
            'salutations': '👋',
            'howdy': '👋',
            'hola': '👋',
            'bonjour': '👋',
            'ciao': '👋',
            'namaste': '👋',
            'welcome back': '👋',
            'good to see you': '👋',
            'ok': '👌',
            'yes': '✅',
            'yeah': '👍',
            'yep': '👍',
            'yup': '👍',
            'sure': '👍',
            'absolutely': '👍',
            'definitely': '👍',
            'certainly': '👍',
            'agreed': '👍',
            'nice': '👌',
            'fine': '👌',
            'cool': '😎',
            'love it': '❤️',
            'thumbs up': '👍',
            'clap': '👏',
            'congrats': '🎉',
            'celebrate': '🎉',
            'cheers': '🥂',
            'high five': '🖐️',
            'bye': '👋',
            'goodbye': '👋',
            'farewell': '👋',
            'see you': '👋',
            'see ya': '👋',
            'see you later': '👋',
            'see you soon': '👋',
            'catch you later': '👋',
            'talk to you later': '👋',
            'till next time': '👋',
            'until we meet again': '👋',
            'take care': '👋',
            'have a good one': '👋',
            'have a great day': '👋',
            'have a nice day': '👋',
            'have a wonderful day': '👋',
            'have a fantastic day': '👋',
            'have a lovely day': '👋',
            'have a pleasant day': '👋',
            'goodnight': '🌙',
            'sweet dreams': '🌙💤',
            'adios': '👋',
            'cheerio': '👋',
            'take it easy': '👋',
            'peace out': '✌️',
            'later': '👋',
            'ttyl': '👋',
            'talk to you soon': '👋',
            'until later': '👋',
            'until next time': '👋',
            'so long': '👋',
            'fare thee well': '👋',
            'be well': '👋',
            'lol': '🤣',
            'lmao': '🤣',
            'lmfao': '🤣',
            'haha': '😄',
            'hehe': '🤭',
            'rofl': '🤣',
            'hahaha': '😄',
            'lolol': '🤣',
            'lolz': '🤣',
            'lmfao': '🤣',
            'lmfaoo': '🤣',
            'bahaha': '😄',
            'bwahaha': '😄',
            'hahah': '😄',
            'hahahaha': '😄',
            'hahahah': '😄',
            'hehehe': '🤭',
            'hehehehe': '🤭',
            'roflmao': '🤣',
            'roflmaoo': '🤣',
            'rotfl': '🤣',
            'teehee': '😄',
            'ha': '😄',
            'haha': '😄',
            'hah': '😄',
            'heheh': '🤭',
            'heheheh': '🤭',
            'ahah': '😄',
            'ahahaha': '😄',
            'ahaha': '😄',
            'ahahah': '😄',
            'ahahaha': '😄',
            'maybe': '🤷',
            'perhaps': '🤷',
            'possibly': '🤷',
            'uncertain': '🤷',
            'undecided': '🤷',
            'unsure': '🤷',
            'dunno': '🤷',
            'not sure': '🤷',
            'no idea': '🤷',
            'no clue': '🤷',
            'i don\'t know': '🤷',
            'idk': '🤷',
            'i have no idea': '🤷',
            'i\'m unsure': '🤷',
            'who knows': '🤷',
            'beats me': '🤷',
            'can\'t say': '🤷',
            'hard to say': '🤷',
            'it\'s up in the air': '🤷',
            'i\'m not certain': '🤷',
            'i\'m not sure': '🤷',
            'i\'m undecided': '🤷',
            'i\'m not convinced': '🤷',
            'i\'m on the fence': '🤷',
            'how are you': '👋',
            'how\'s it going': '🤔',
            'hru': '🤷',
            'how are u': '👋',
            'how are ya': '🤷',
            'how\'s life': '🌟',
            'how have you been': '🤔',
            'what\'s up': '👋',
            'what\'s new': '🌟',
            'how\'s everything': '🌟',
            'how do you do': '👋',
            'are you okay': '🤷',
            'r u ok': '🤷',
            'how\'s your day': '🌞',
            'how\'s your day going': '🌞',
            'how\'s your day been': '🌞',
            'how\'s your day so far': '🌞',
            'how\'s your week': '📆',
            'how\'s your weekend': '🌴',
            'how are things': '🤷',
            'how\'s your health': '🌡️',
            'how\'s your mood': '😊',
            'how\'s your spirit': '✨',
            'nvm': '🙅',
            'never mind': '🙅',
            'forget it': '🙅',
            'ignore': '🙈',
            'disregard': '🙉',
            'skip': '⏭️',
            'pass': '⏭️',
            'not important': '🤷',
            'not relevant': '🤷‍',
            'not interested': '🤷‍',
            'don\'t care': '🤷‍',
            'let it go': '🧘',
            'nothing': '😐',
            'nope': '🙅‍',
            'ignore me': '🙈',
            'disregard me': '🙉',
            'not important to me': '🤷‍',
            'not relevant to me': '🤷‍',
            'I don\'t care': '🤷',
            'let me go': '🧘',
            'don\'t bother': '🙅',
            'bruh': '🗿',
            'oof': '🙃',
            'yikes': '😬',
            'facepalm': '🤦',
            'disappointed': '😞',
            'disaster': '💥',
            'fail': '👎',
            'epic fail': '🤦',
            'disaster': '😱',
            'tragic': '😢',
            'awful': '😖',
            'terrible': '😫',
            'horrible': '😣',
            'cringe': '🤢',
            'oh no': '😱',
            'disappointing': '😕',
            'regrettable': '😔',
            'shocking': '😳',
            'unexpected': '😮',
            'unbelievable': '🤯',
            'chaos': '🌪️',
            'nightmare': '🌙',
            'mess': '🧹',
            'botch': '🤪',
            'sloppy': '🤷',
            'disorganized': '🌀',
            'unprofessional': '🤦',
            
        }

        for word, emoji in reactions.items():
            if message.content.lower() == word:
                await message.add_reaction(emoji)  # React with the corresponding emoji

        if message.content.endswith('?'):
            await message.add_reaction('❓')  # React with a question mark
    if not message.author.bot:
        if isinstance(message.channel, discord.DMChannel):
            if afk_reason is not None:
                reply_message = f"Sorry, I am currently AFK with the reason: {afk_reason}."
                await message.author.send(reply_message)
        else:
            if bot.user in message.mentions:
                if afk_reason is not None:
                    reply_message = f"Sorry, **{message.author.name}**, I am currently AFK with the reason: {afk_reason}."
                    await message.channel.send(reply_message)

    await bot.process_commands(message)

# Bot Help

categories = {
    1: {
        "name": "Nuking and Raiding",
        "commands": [
            "+spam <ammount> <message>",
            "+raid <message>",
            "+delete_all_roles",
            "+delete_all_channels",
            "+nuke",
            "+hackclear",
            "+prune",
            "+masskick <server_id>"
        ]
    },
    2: {
        "name": "Server Management",
        "commands": [
            "+server",
            "+set_server_banner <link>",
            "+set_server_avatar <link>",
            "+clone_channels <old_server_id> <new_server_id>",
            "+clone_roles <old_server_id> <new_server_id>",
            "+clone_server <old_server_id> <new_server_id>"
        ]
    },
    3: {
        "name": "Moderation and Utilities",
        "commands": [
            "+clear <ammount>",
            "+avatar <user_id>",
            "+banner <user_id>",
            "+react <message_id> <emoji>",
            "+block <user_id or user_mention>",
            "+unblock <user_id or user_mention>",
            "+leave"
        ]
    },
    4: {
        "name": "Giveaways and Polls",
        "commands": [
            "+gend <message_id>",
            "+gstart <durations> <winners_ammount> <prize>",
            "+poll <poll_name>, <question>, <option_1>, <option_2>, <option_N>"
        ]
    },
    5: {
        "name": "Personalization",
        "commands": [
            "+status",
            "+stop_status",
            "+mode <type> <message>",
            "+set_avatar <link>",
            "+set_banner <link>"
        ]
    },
    6: {
        "name": "Fun and Miscellaneous",
        "commands": [
            "+tf <text>",
            "+ping <ammount> <message>",
            "+nitro",
            "+spamthreadsall <ammount> <name>",
            "+f1 <text>",
            "+AFK <reason>",
            "+unAFK",
            "+hjoin",
            "+send_avatars",
            "+send_animated_avatars",
            "+send_banners",
            "+link_to_file <channel_id>",
            "+asci <text>"
        ]
    }
}

@bot.command()
async def commands(ctx, category_number: int = None):
    await ctx.message.delete()
    if category_number is None:
        help_message = "**ERROR SELF BOT**\n\n"
        for category_number, category_data in categories.items():
            help_message += f"{category_number}. {category_data['name']}\n"
        help_message += "\n**Select a category using `+commands <category_number>` **"
        await ctx.send(help_message)
    else:
        if category_number in categories:
            category_data = categories[category_number]
            category_name = category_data["name"]
            category_commands = category_data["commands"]
            help_message = f"**Category: {category_name}**\n\n"
            for command in category_commands:
                help_message += f"{command}\n"
            help_message += f"\n **ERROR SELF BOT**"
            await ctx.send(help_message)
        else:
            await ctx.send("Invalid category number")

# Bot Commands 

# Nuking and Raiding

# 1. SPAM
@bot.command()
async def spam(ctx, amount: int, *, message: str):
    for _ in range(amount):
        await ctx.send(message)
# 2. RAID
@bot.command(hidden=True)
async def raid(ctx, *, message: str):
    """Spams a message in all text channels.

    Args:
        ctx (commands.Context): the command context
        message (str): the message to send for spamming.
    """

    def check_reply(reply) -> bool:
        return reply.content.lower() == 'stop' and reply.author == ctx.author

    async def spam_text() -> None:
        while True:
            tasks = [channel.send(message) for channel in ctx.guild.text_channels]
            await asyncio.gather(*tasks, return_exceptions=True)

    await ctx.message.delete()

    if not message.strip():
        await ctx.send("You must provide a message to spam.")
        return

    await ctx.send(f"Started raiding: {message}")

    spam_task = bot.loop.create_task(spam_text())
    await bot.wait_for('message', check=check_reply)
    spam_task.cancel()

    await ctx.send("Stopped raiding.")
# 3. DELETE ALL ROLES
@bot.command()
async def delete_all_roles(ctx):
    """
    Deletes all roles in the server, except the @everyone role.
    Usage: !delete_all_roles
    """
    server = ctx.guild

    if server is None:
        await ctx.send("The server does not exist.")
        return

    roles = server.roles

    for role in roles:
        if role.name != "@everyone":  # Skip the @everyone role
            try:
                await role.delete(reason="Deleting all roles")
            except Exception as e:
                print(f"Failed to delete role {role.name}: {e}")

    await ctx.send("All roles have been deleted successfully!")
# 4. DELETE ALL CHANNELS
@bot.command()
async def delete_all_channels(ctx):
    """
    Deletes all channels and categories in the server.
    Usage: !delete_all_channels
    """
    server = ctx.guild

    # Loop through each category in the server
    for category in server.categories:
        # Delete the category
        await category.delete()

    # Loop through each text channel in the server
    for text_channel in server.text_channels:
        # Delete the text channel
        await text_channel.delete()

    # Loop through each voice channel in the server
    for voice_channel in server.voice_channels:
        # Delete the voice channel
        await voice_channel.delete()

    await ctx.send('All channels and categories deleted.')
# 5. NUKE
@bot.command()
async def nuke(ctx):
    """
    Deletes all roles, channels, and categories in the server.
    Usage: !delete_all_server
    """
    # Call the delete_all_roles command
    await delete_all_roles(ctx)

    # Call the delete_all_channels command
    await delete_all_channels(ctx)

    await ctx.send('All roles, channels, roles, and categories have been deleted successfully!')
# 6. Hack Clear
@bot.command()
async def hackclear(ctx):
    await ctx.send("⠀" + "\n"*1998 + "⠀")
    await ctx.message.delete()
#7 Prune
@bot.command()
async def prune(ctx):
    await ctx.reply("pruning....")
    time.sleep(2)
    await ctx.guild.prune_members(days=1, compute_prune_count=False, roles=ctx.guild.roles)
    time.sleep(1)
    await ctx.reply("**Successfully Pruned.**")
      
#8 MassKick
@bot.command()
async def masskick(ctx, guild_id):
    guild = bot.get_guild(int(guild_id))
    if guild is None:
        await ctx.reply("Invalid guild ID provided.", mention_author=True)
        return

    await bot.wait_until_ready()
    try:
        os.remove('members.txt')
    except:
        pass

    membercount = 0
    with open('members.txt', 'a') as m:
        for member in guild.members:
            m.write(str(member.id) + '\n')
            membercount += 1

        await ctx.reply(f'ERROR SELF BOT | MASS KICK INITIATED\nRemoving {membercount} Members in progress......', mention_author=True)

    guild_id = str(guild_id)
    print()
    headers = mainHeader()

    with open('members.txt') as members_file:
        for member_id in members_file:
            while True:
                r = requests.delete(f"https://discord.com/api/v8/guilds/{guild_id}/members/{member_id.strip()}", headers=headers)
                if 'retry_after' in r.text:
                    time.sleep(r.json()['retry_after'])
                else:
                    if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                        print(f"Kicked {member_id.strip()}")
                        break
                    else:
                        break

    await ctx.reply(f'Mass kick completed. Kicked {membercount} members.', mention_author=True)

# Server Management

# 1. Server
@bot.command(aliases=['server'])
async def guild(ctx):
    bots = 0
    users = 0
    for member in ctx.guild.members:
        if member.bot:
            bots += 1
        else:
            users += 1
    
    created_at = ctx.guild.created_at.replace(tzinfo=timezone.utc)
    time_ago = humanize.naturaltime(datetime.now(timezone.utc) - created_at)
    
    total_channels = len(ctx.guild.channels) - len(ctx.guild.categories)
    
    await ctx.message.edit(content=f"__**Self Bot created by Harry Uchiha**__\n\n"
                                   "╰────╮Basic ✯\n"
                                   f"🜲┌ **Name**: `{ctx.guild.name}`\n"
                                   f"🜲├ **ID**: `{ctx.guild.id}`\n"
                                   f"🜲├ **Owner**: `{ctx.guild.owner}` - (`{ctx.guild.owner.id}`)\n"
                                   f"🜲└ **Created at**: {created_at} ({time_ago})\n"
                                   "╰────╮Member And Bot Info ✯\n"
                                   f"ඞ┌ **Total**: `{users + bots}`\n"
                                   f"ඞ├ **Members**: `{users}`\n"
                                   f"ඞ└ **Bots**: `{bots}`\n"
                                   "╰────╮Channels Info ✯\n"
                                   f"☆┌ **Channels**: `{total_channels}`\n"
                                   f"☆├ **Text**: `{len(ctx.guild.text_channels)}`\n"
                                   f"☆├ **Voice**: `{len(ctx.guild.voice_channels)}`\n"
                                   f"☆└ **Categories**: `{len(ctx.guild.categories)}`")
# 2. Set Server Avatar 
@bot.command()
async def set_server_avatar(ctx, link):
    """
    Set the server's avatar from a URL.
    Usage: +set_server_avatar <url_to_image>
    Image URL must be a .png, a .jpg, or a .gif
    """
    url = link
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for any request errors
    except requests.HTTPError:
        await ctx.send("Failed to retrieve the image from the provided URL.")
        return

    img = io.BytesIO()
    for block in response.iter_content(1024):
        if not block:
            break

        img.write(block)

    if url:
        img.seek(0)
        imgbytes = img.read()
        img.close()

        try:
            await ctx.guild.edit(icon=imgbytes)
            await ctx.send("The server's avatar has been updated.")
        except discord.errors.HTTPException:
            await ctx.send("Failed to update the server's avatar. Please ensure the image is in the correct format.")
    else:
        await ctx.send("Could not find image.")
# 3. Set Banner Avatar
@bot.command()
async def set_server_banner(ctx, link):
    try:
        guild = ctx.guild
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    if resp.status != 200:
                        return await ctx.send('Error: Invalid image URL.')

                    data = await resp.read()
                    with open('temp_banner.png', 'wb') as file:
                        file.write(data)

            with open('temp_banner.png', 'rb') as file:
                await guild.edit(banner=file.read())

            await ctx.send("Server banner background has been updated successfully!")

            os.remove('temp_banner.png')  # Remove the temporary file
    except Exception as e:
        await ctx.send(f"An error occurred while updating the server banner background: {e}")
# 4. Clone Channels
@bot.command()
async def clone_channels(ctx, old_server_id: int, new_server_id: int):
    """
    Clones channels and categories from an old server to a new server with the same permissions.
    Usage: !clone_channel <old_server_id> <new_server_id>
    """
    # Fetch the old server and new server
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)

    if not old_server:
        await ctx.send('Old server not found.')
        return
    if not new_server:
        await ctx.send('New server not found.')
        return

    # Loop through each category in the old server
    for old_category in old_server.categories:
        # Create a new category in the new server with the same name and permissions
        new_category = await new_server.create_category_channel(name=old_category.name, overwrites=old_category.overwrites)

        # Loop through each text channel in the old category
        for old_text_channel in old_category.text_channels:
            # Create a new text channel in the new category with the same name and permissions
            new_text_channel = await new_category.create_text_channel(name=old_text_channel.name, overwrites=old_text_channel.overwrites)

            # Send a confirmation message
            await ctx.send(f'Text channel cloned: {old_text_channel.name} -> {new_text_channel.name} in category: {old_category.name} -> {new_category.name}')
        
        # Loop through each voice channel in the old category
        for old_voice_channel in old_category.voice_channels:
            # Create a new voice channel in the new category with the same name and permissions
            new_voice_channel = await new_category.create_voice_channel(name=old_voice_channel.name, overwrites=old_voice_channel.overwrites)

            # Send a confirmation message
            await ctx.send(f'Voice channel cloned: {old_voice_channel.name} -> {new_voice_channel.name} in category: {old_category.name} -> {new_category.name}')
# 5. Clone Roles
@bot.command()
async def clone_roles(ctx, old_server_id: int, new_server_id: int):
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)

    if old_server is None:
        await ctx.send("The old server does not exist.")
        return

    if new_server is None:
        await ctx.send("The new server does not exist.")
        return

    old_roles = old_server.roles

    role_map = {}

    for role in reversed(old_roles):  # Iterate in reverse order
        new_role = await new_server.create_role(name=role.name, color=role.color, hoist=role.hoist,
                                               mentionable=role.mentionable, permissions=role.permissions,
                                               reason="Cloning roles")
        role_map[role.id] = new_role
        await ctx.send(f'Role cloned: {role.name} -> {new_role.name}')

    for member in old_server.members:
        member_roles = member.roles
        new_member = new_server.get_member(member.id)
        if new_member is not None:
            for role in reversed(member_roles):  # Iterate in reverse order
                if role.id in role_map:
                    new_role = role_map[role.id]
                    await new_member.add_roles(new_role)

    await ctx.send("Roles have been cloned successfully!")
# 6. Clone Server
@bot.command()
async def clone_server(ctx, old_server_id: int, new_server_id: int):
    """
    Clones channels, categories, and roles from an old server to a new server with the same permissions.
    Usage: !clone_server <old_server_id> <new_server_id>
    """
    # Fetch the old server and new server
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)

    if not old_server:
        await ctx.send('Old server not found.')
        return
    if not new_server:
        await ctx.send('New server not found.')
        return

    # Clone channels and categories
    for old_category in old_server.categories:
        new_category = await new_server.create_category_channel(name=old_category.name, overwrites=old_category.overwrites)

        for old_text_channel in old_category.text_channels:
            new_text_channel = await new_category.create_text_channel(name=old_text_channel.name, overwrites=old_text_channel.overwrites)
            await ctx.send(f'Text channel cloned: {old_text_channel.name} -> {new_text_channel.name} in category: {old_category.name} -> {new_category.name}')
        
        for old_voice_channel in old_category.voice_channels:
            new_voice_channel = await new_category.create_voice_channel(name=old_voice_channel.name, overwrites=old_voice_channel.overwrites)
            await ctx.send(f'Voice channel cloned: {old_voice_channel.name} -> {new_voice_channel.name} in category: {old_category.name} -> {new_category.name}')

    # Clone roles
    old_roles = old_server.roles
    role_map = {}

    for role in reversed(old_roles):
        new_role = await new_server.create_role(name=role.name, color=role.color, hoist=role.hoist,
                                               mentionable=role.mentionable, permissions=role.permissions,
                                               reason="Cloning roles")
        role_map[role.id] = new_role
        await ctx.send(f'Role cloned: {role.name} -> {new_role.name}')

    for member in old_server.members:
        member_roles = member.roles
        new_member = new_server.get_member(member.id)
        if new_member is not None:
            for role in reversed(member_roles):
                if role.id in role_map:
                    new_role = role_map[role.id]
                    await new_member.add_roles(new_role)

    await ctx.send("Server cloned successfully!")


# Moderation and Utilities

# 1. clear
@bot.command()
async def clear(ctx, amount: int):
    def is_bot_message(message):
        return message.author == bot.user

    messages = []
    if isinstance(ctx.channel, discord.TextChannel):
        async for message in ctx.channel.history(limit=None):
            if is_bot_message(message):
                messages.append(message)
                if len(messages) == amount + 1:
                    break
        await ctx.channel.delete_messages(messages)
    elif isinstance(ctx.channel, discord.DMChannel):
        async for message in ctx.channel.history(limit=None):
            if is_bot_message(message):
                messages.append(message)
                if len(messages) == amount + 1:
                    break
        for message in messages:
            await message.delete()
# 2. avatar
@bot.command()
async def avatar(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    avatar_url = str(user.avatar.url)
    try:
        await ctx.send(avatar_url)
        await ctx.message.add_reaction('<a:v_:1105968883833241742>')  # React with a success emoji
    except discord.errors.HTTPException:
        await ctx.message.add_reaction('❌')  # React with a failure emoji
# 3. banner
@bot.command()
async def banner(ctx):
    banner_url = str(bot.user.banner.url)
    try:
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send(banner_url)
        elif isinstance(ctx.channel, discord.TextChannel):
            await ctx.send(banner_url)
        await ctx.message.add_reaction('<a:v_:1105968883833241742>')  # React with a success emoji
    except discord.errors.HTTPException:
        await ctx.message.add_reaction(':skull:')  # React with a failure emoji
# 4. react
@bot.command()
async def react(ctx, message_id: int, reaction: str):
    message = None

    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                message = await channel.fetch_message(message_id)
                break
            except discord.NotFound:
                pass

    if message is None:
        await ctx.send('Message not found.')
        return

    try:
        await message.add_reaction(reaction)
        await ctx.send(f'Reaction {reaction} added to the message.')
    except discord.NotFound:
        await ctx.send('Emoji not found.')
    except discord.Forbidden:
        await ctx.send('I do not have permission to add reactions.')
# 5. block
@bot.command()
async def block(ctx, user: discord.User):
    member = user

    await ctx.send(f'Blocked {user.name}#{user.discriminator}')
    await member.block()
# 6. unblock
@bot.command()
async def unblock(ctx, user: discord.User):
    member = user

    await ctx.send(f'Unblocked {user.name}#{user.discriminator}')
    await member.unblock()
# 7. Leave
@bot.command()
async def leave(ctx):
    await ctx.message.add_reaction('✅')  # React with a tick emoji
    guild = ctx.guild
    if guild.owner == bot.user:
        await ctx.send("I see that I am the owner of this server. Are you sure you want to delete it? Reply with 'YES' to proceed.")
        try:
            response = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
            if response.content.upper() == 'YES':
                await ctx.send("Deleting the server. Goodbye!")
                await guild.delete()
            else:
                await ctx.send("Server deletion has been revoked. Phew, that was a close call!")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Server deletion has been revoked.")
    else:
        await ctx.send("Leaving the server. Goodbye!")
        await guild.leave()

# Giveaways and Polls

# Giveaway End
@bot.command()
async def gend(ctx, message_id: int):
    try:
        message = await ctx.channel.fetch_message(message_id)  # Fetch the message by ID
    except discord.NotFound:
        await ctx.send("Invalid message ID.")
        return
    
    if not message.reactions:
        await ctx.send("The specified message has no reactions.")
        return
    
    reaction = random.choice(message.reactions)  # Select a random reaction
    
    emoji = str(reaction.emoji)  # Get the emoji as a string
    
    participants = []
    async for user in reaction.users():
        participants.append(user)
    
    if len(participants) > 0:
        winner = random.choice(participants)  # Select a random winner
        await ctx.send(f"The winner is {winner.mention} with the reaction {emoji}!")
    else:
        await ctx.send("No participants found for the reaction.")
# Giveaway Start
@bot.command()
async def gstart(ctx, duration, winners: int, *, prize):
    await ctx.message.delete()  # Delete the command message

    time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}  # Conversion rates for time units
    time_amount = int(duration[:-1]) * time_units[duration[-1].lower()]  # Extracting the time amount and unit

    end_time = datetime.utcnow() + timedelta(seconds=time_amount)
    timestamp_format = "%Y-%m-%d %H:%M:%S"

    message = f"🎉 **Giveaway** 🎉\n\n> Prize: {prize}\n> Hosted by: {ctx.author.mention}\n> Winners: {winners}\n> Ends in: <t:{int(end_time.timestamp())}:R>"

    giveaway_message = await ctx.send(message)
    await giveaway_message.add_reaction("🎉")

    await asyncio.sleep(time_amount)

    updated_message = await ctx.fetch_message(giveaway_message.id)
    reaction = discord.utils.get(updated_message.reactions, emoji="🎉")

    participants = []
    async for user in reaction.users():
        participants.append(user)

    participants.remove(bot.user)  # Remove the bot from participants list

    if len(participants) <= winners:
        winners = len(participants)

    winner_list = random.sample(participants, winners)  # Select random winners

    winner_mentions = [winner.mention for winner in winner_list]
    winner_text = ", ".join(winner_mentions)

    result_message = f"🎉 Giveaway ended! Winners: {winner_text}"
    await ctx.send(result_message)
# Poll
@bot.command()
async def poll(ctx, *, args):
    await ctx.message.delete()

    split_args = args.split(',')

    split_args = [arg.strip() for arg in split_args]

    if len(split_args) < 4 or len(split_args) > 7:
        await ctx.send("Please provide between 2 and 5 options.")
        return

    name = split_args[0]
    question = split_args[1]
    options = split_args[2:]

    if len(name) > 20:
        await ctx.send("Poll name must be up to 20 characters.")
        return

    poll_message = f"<a:GG_mh:1104067405904363633> **POLL : {name}** <a:GG_mh:1104067405904363633>\n"
    poll_message += f"<a:v_:1105968883833241742> **{question}** <a:v_:1105968883833241742>\n"
    poll_message += "┌✦✦ <:ac:1107466412060057722>\n"

    emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

    for i, option in enumerate(options):
        emoji = emoji_list[i] if i < len(emoji_list) else ""
        option_with_commas = option.replace(',', ' ')
        poll_message += f"├{emoji} | {option_with_commas}\n"

    poll_message += "└✦✦ <:ac:1107466412060057722>"

    poll_msg = await ctx.send(poll_message)

    for i in range(len(options)):
        emoji = emoji_list[i] if i < len(emoji_list) else ""
        await poll_msg.add_reaction(emoji)


# Personalization

# STATUS
@bot.command()
async def status(ctx):
    global status_changing  # Declare the flag as global

    if status_changing:
        await ctx.send("Status changing is already in progress.")
        return

    await ctx.send("After how much time do you want the status to swap")
    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    try:
        changing_time = await bot.wait_for('message', check=check, timeout=60)
        changing_time = int(changing_time.content)
    except asyncio.TimeoutError:
        await ctx.send("No response received. Please try again.")
        return
    
    await ctx.send("How many statuses do you want to add")
    
    try:
        num_statuses = await bot.wait_for('message', check=check, timeout=60)
        num_statuses = int(num_statuses.content)
    except asyncio.TimeoutError:
        await ctx.send("No response received. Please try again.")
        return
    
    if num_statuses <= 0:
        await ctx.send("Please provide a positive number of statuses.")
        return
    
    statuses.clear()
    
    for i in range(1, num_statuses + 1):
        await ctx.send(f"Write status {i}:")
        try:
            status = await bot.wait_for('message', check=check, timeout=120)
            parsed_status = status.content.strip()
            statuses.append(parsed_status)
        except asyncio.TimeoutError:
            await ctx.send(f"No response received for status {i}. Please try again.")
            return
    
    await ctx.send("Status changing has started.")
    status_changing = True 
    
    while status_changing:  
        for status in statuses:
            await bot.change_presence(activity=discord.CustomActivity(name=status))
            await asyncio.sleep(changing_time)
            if not status_changing:
                break
# STOP STATUS
@bot.command()
async def stop_status(ctx):
    global status_changing 

    if not status_changing:
        await ctx.send("Status changing is not in progress.")
        return

    await ctx.send("Stopping the status changing.")
    status_changing = False 
# Rich Status
@bot.command(aliases=['mode'])
async def rich_status(ctx, activity_type, *, text):
    await ctx.message.delete()
    activity = None
    if activity_type == 'playing':
        activity = discord.Game(name=text)
    elif activity_type == 'streaming':
        activity = discord.Streaming(name=text, url='https://www.twitch.tv/devilharisyt')
    elif activity_type == 'listening':
        activity = discord.Activity(type=discord.ActivityType.listening, name=text)
    elif activity_type == 'watching':
        activity = discord.Activity(type=discord.ActivityType.watching, name=text)

    if activity:
        await bot.change_presence(activity=activity)
        await ctx.send(f'**Status updated**\n\n> TYPE : **{activity_type}**\n> TEXT: **{text}**\n\n**Selfbot by ZenTirog**')
    else:
        await ctx.send('Invalid activity type. Available types: playing, streaming, listening, watching')
# SET AVATAR
@bot.command()
async def set_avatar(ctx, link):
    """
    Set an avatar from a URL.
    Usage: +set_avatar <url_to_image>
    Image URL must be a .png, a .jpg, or a .gif (nitro only)
    """
    url = link
    if ".gif" in url and not bot.user.premium:
        await ctx.send(f"Warning: attempting to copy an animated avatar without Nitro. Only the first frame will be set.")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  
    except requests.HTTPError:
        await ctx.send(f"Failed to retrieve the image from the provided URL.")
        return

    img = io.BytesIO()
    for block in response.iter_content(1024):
        if not block:
            break

        img.write(block)

    if url:
        img.seek(0)
        imgbytes = img.read()
        img.close()
        try:
            await bot.user.edit(avatar=imgbytes)
            await ctx.send(f"Your avatar has been set to the specified image.")
        except discord.errors.HTTPException:
            await ctx.send(f"You are being rate-limited!")
    else:
        await ctx.send(f"Could not find image.")
# SET BANNER
@bot.command()
async def set_banner(ctx, link):
    """
    Set a banner from a URL.
    Usage: +set_banner <url_to_image>
    Image URL must be a .png, a .jpg, or a .gif (nitro only)
    """
    url = link
    if ".gif" in url and not bot.user.premium:
        await ctx.send("Warning: attempting to copy an animated banner without Nitro. Only the first frame will be set.")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.HTTPError:
        await ctx.send("Failed to retrieve the image from the provided URL.")
        return

    img = io.BytesIO()
    for block in response.iter_content(1024):
        if not block:
            break
        img.write(block)

    img.seek(0)
    imgbytes = img.read()
    img.close()

    try:
        await bot.user.edit(banner=imgbytes)
        await ctx.send("Your banner has been set to the specified image.")
    except discord.errors.HTTPException:
        await ctx.send("You are being rate-limited!")

# Fun and Miscellaneous

# Text Flip
@bot.command()
async def tf(ctx, *, msg):
    """Flip given text."""
    text_flip = {
        'a': 'ɐ',
        'b': 'q',
        'c': 'ɔ',
        'd': 'p',
        'e': 'ǝ',
        'f': 'ɟ',
        'g': 'ƃ',
        'h': 'ɥ',
        'i': 'ᴉ',
        'j': 'ɾ',
        'k': 'ʞ',
        'l': 'l',
        'm': 'ɯ',
        'n': 'u',
        'o': 'o',
        'p': 'd',
        'q': 'b',
        'r': 'ɹ',
        's': 's',
        't': 'ʇ',
        'u': 'n',
        'v': 'ʌ',
        'w': 'ʍ',
        'x': 'x',
        'y': 'ʎ',
        'z': 'z',
        'A': '∀',
        'B': 'q',
        'C': 'Ɔ',
        'D': 'p',
        'E': 'Ǝ',
        'F': 'Ⅎ',
        'G': 'פ',
        'H': 'H',
        'I': 'I',
        'J': 'ſ',
        'K': 'ʞ',
        'L': '˥',
        'M': 'W',
        'N': 'N',
        'O': 'O',
        'P': 'Ԁ',
        'Q': 'Q',
        'R': 'ᴚ',
        'S': 'S',
        'T': '⊥',
        'U': '∩',
        'V': 'Λ',
        'W': 'M',
        'X': 'X',
        'Y': '⅄',
        'Z': 'Z',
        '0': '0',
        '1': 'Ɩ',
        '2': 'ᄅ',
        '3': 'Ɛ',
        '4': 'ㄣ',
        '5': 'ϛ',
        '6': '9',
        '7': 'ㄥ',
        '8': '8',
        '9': '6',
        '.': '˙',
        ',': "'",
        "'": ',',
        '"': ',,',
        '`': ',',
        '(': ')',
        ')': '(',
        '[': ']',
        ']': '[',
        '{': '}',
        '}': '{',
        '?': '¿',
        '!': '¡',
        '<': '>',
        '>': '<',
        '&': '⅋',
        '_': '‾',
        ';': '؛',
        '∴': '∵',
        '‿': '⁀',
        '⁅': '⁆',
        '∣': '∤',
        '∓': '∓',
        '∠': '∟',
        '⊂': '⊃',
        '⊆': '⊇',
        '≤': '≥',
        '≥': '≤',
        '≠': '≠',
        '+': '±',
        '-': '⁻',
        '=': 'ƚ',
        '♭': '♯',
        '$': '￥',
        '¢': '€',
        '∞': '∞',
        'ɐ': 'a',
        'ɔ': 'c',
        'ǝ': 'e',
        'ɟ': 'f',
        'ƃ': 'g',
        'ɥ': 'h',
        'ᴉ': 'i',
        'ɾ': 'j',
        'ʞ': 'k',
        'ʍ': 'w',
        'ʇ': 't',
        '˥': 'l',
        'ɯ': 'm',
        'ʌ': 'v',
        'ʎ': 'y',
        '¿': '?',
        '¡': '!',
        '﹫': '@',
        '‾': '_',
        '˚': 'ø',
        'ø': 'o',
        'ₒ': 'o',
        'Ỗ': 'O',
        'ᴼ': 'O',
        'ᵒ': 'o',
        '∘': 'o',
        'Ｏ': 'O',
        'ᴏ': 'o',
        'ｏ': 'o',
        'ò': 'o',
        'ó': 'o',
        'ô': 'o',
        'õ': 'o',
        'ö': 'o',
        'ō': 'o',
        'ø': 'o',
        'ǒ': 'o',
        'ő': 'o',
        'ŏ': 'o',
        'ȯ': 'o',
        'ȍ': 'o',
        'ơ': 'o',
        'ớ': 'o',
        'ờ': 'o',
        'ỡ': 'o',
        'ở': 'o',
        'ợ': 'o',
        'ọ': 'o',
        'ộ': 'o',
        'ồ': 'o',
        'ố': 'o',
        'ỗ': 'o',
        'ộ': 'o',
        'ǫ': 'o',
        'ǭ': 'o',
        'ǿ': 'o',
        'œ': 'o',
        'ᴐ': 'o',
        'ᴑ': 'o',
        'ﺄ': 'ا',
        'ﺈ': 'ا',
        'ﺌ': 'ا',
        'ﺎ': 'ا',
        'ﺄ': 'أ',
        'ﺈ': 'أ',
        'ﺌ': 'أ',
        'ﺎ': 'أ',
        'ﺂ': 'آ',
        'ﺂ': 'ء',
        'ﺎ': 'ئ',
        'ﺎ': 'ؤ',
        'ﺎ': 'ء',
        'ₐ': 'a',
        'ₑ': 'e',
        'ₓ': 'x',
        'ₕ': 'h',
        'ₖ': 'k',
        'ₗ': 'l',
        'ₘ': 'm',
        'ₙ': 'n',
        'ₒ': 'o',
        'ₚ': 'p',
        'ᵣ': 'r',
        'ₛ': 's',
        'ₜ': 't',
        'ᵤ': 'u',
        'ᵥ': 'v',
        'ₓ': 'x',
    }
    result = ""
    for char in msg:
        if char in text_flip:
            result += text_flip[char]
        else:
            result += char
    await ctx.message.edit(content=result[::-1])
# PING
@bot.command()
async def ping(ctx, amount: int, *, message: str):
    await ctx.message.delete()  # Delete the command message

    for _ in range(amount):
        sent_message = await ctx.send(message)
        await sent_message.delete()
# Nitro
@bot.command()
async def nitro(ctx, amount: int = 100_000, nitrotype='classic'):
    await ctx.message.edit(content=f'**__Selfbot by ERROR\n\Generating {amount} Nitro Codes...**')
    with open(f'{amount}_nitro_codes.txt', 'w', encoding='utf-8') as f:
        f.write('Selfbot by Harry\ndiscord.gg/legitreward\n--------------------------------------------\n')
        count = 24
        if nitrotype == 'classic':
            count = 16
        for i in range(amount):
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=count))
            f.write(f'discord.gift/{code}\n')
        f.write('--------------------------------------------\nSelfbot by ERROR\ndiscord.gg/maceters')
    await ctx.send(f'**__Selfbot by ERROR__\n\n:crown: Generated {amount} Nitro Codes!**', file=discord.File(f'{amount}_nitro_codes.txt'))
    await ctx.message.delete()
# Spam Threads
@bot.command(aliases=['spamthreadall', 'spamthreads', 'threadsspamall'])
async def spamthreadsall(ctx, amount: int, *, name):
    await ctx.message.delete()
    success_count = 0
    error = False

    for i in range(amount):
        for channel in ctx.guild.text_channels:
            while True:
                try:
                    thread = await channel.create_thread(name=name, auto_archive_duration=1440)
                    success_count += 1
                    break
                except discord.Forbidden:
                    await asyncio.sleep(1)  # Delay to avoid hitting rate limits
                except discord.HTTPException as e:
                    error = True
                    await ctx.send(f"**__Bot by ERROR__\n\nError :x:\n```Error code: {e.status}\n{e.text}```**")
                    break

    if not error:
        await ctx.send(f"**__Bot by ERROR__\n\n:white_flower: Successfully created {success_count} threads in each channel!**")
# Font 1
@bot.command()
async def f1(ctx, *, msg):
    """Convert given text to small text."""
    small_text = {
        'a': 'ᴀ',
        'b': 'ʙ',
        'c': 'ᴄ',
        'd': 'ᴅ',
        'e': 'ᴇ',
        'f': 'ꜰ',
        'g': 'ɢ',
        'h': 'ʜ',
        'i': 'ɪ',
        'j': 'ᴊ',
        'k': 'ᴋ',
        'l': 'ʟ',
        'm': 'ᴍ',
        'n': 'ɴ',
        'o': 'ᴏ',
        'p': 'ᴘ',
        'q': 'Q',
        'r': 'ʀ',
        's': 'ꜱ',
        't': 'ᴛ',
        'u': 'ᴜ',
        'v': 'ᴠ',
        'w': 'ᴡ',
        'x': 'x',
        'y': 'ʏ',
        'z': 'ᴢ',
        'A': 'ᴀ',
        'B': 'ʙ',
        'C': 'ᴄ',
        'D': 'ᴅ',
        'E': 'ᴇ',
        'F': 'ꜰ',
        'G': 'ɢ',
        'H': 'ʜ',
        'I': 'ɪ',
        'J': 'ᴊ',
        'K': 'ᴋ',
        'L': 'ʟ',
        'M': 'ᴍ',
        'N': 'ɴ',
        'O': 'ᴏ',
        'P': 'ᴘ',
        'Q': 'Q',
        'R': 'ʀ',
        'S': 'ꜱ',
        'T': 'ᴛ',
        'U': 'ᴜ',
        'V': 'ᴠ',
        'W': 'ᴡ',
        'X': 'x',
        'Y': 'ʏ',
        'Z': 'ᴢ',
        '0': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '.': '.',
        ',': ',',
        "'": "'",
        '"': '"',
        '`': '`',
        '(': '(',
        ')': ')',
        '[': '[',
        ']': ']',
        '{': '{',
        '}': '}',
        '?': '?',
        '!': '!',
        '<': '<',
        '>': '>',
        '&': '&',
        '_': '_',
        ';': ';',
        '∴': '∴',
        '‿': '‿',
        '⁅': '⁅',
        '∣': '∣',
        '∓': '∓',
        '∠': '∠',
        '⊂': '⊂',
        '⊆': '⊆',
        '≤': '≤',
        '≥': '≥',
        '≠': '≠',
        '+': '+',
        '-': '-',
        '=': '=',
        '♭': '♭',
        '$': '$',
        '¢': '¢',
        '∞': '∞',
        'ɐ': 'ᴀ',
        'ɔ': 'ᴄ',
        'ǝ': 'ᴇ',
        'ɟ': 'ꜰ',
        'ƃ': 'ɢ',
        'ɥ': 'ʜ',
        'ᴉ': 'ɪ',
        'ɾ': 'ᴊ',
        'ʞ': 'ᴋ',
        'ʍ': 'ᴡ',
        'ʇ': 'ᴛ',
        '˥': 'ʟ',
        'ɯ': 'ᴍ',
        'ʌ': 'ᴠ',
        'ʎ': 'ʏ',
    }

    converted_text = []
    for char in msg:
        converted_char = small_text.get(char, char)
        converted_text.append(converted_char)

    await ctx.send(''.join(converted_text))
# AFK
@bot.command()
async def AFK(ctx, *, reason):
    global afk_reason
    afk_reason = reason
    message = f"I am now AFK with the reason: {reason}."
    await ctx.send(message)
# UNAFK
@bot.command()
async def unAFK(ctx):
    global afk_reason
    afk_reason = None
    message = "I am no longer AFK."
    await ctx.send(message)
# HypeSquad Joiner
@bot.command()
async def hjoin(ctx):
    await ctx.send('''Choose a HypeSquad house:
1. Bravery
2. Brilliance
3. Balance
4. Leave The HypeSquad''')

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        choice = await bot.wait_for('message', check=check, timeout=30)
        house = choice.content

        if house == '1':
            housefinal = '1'
        elif house == '2':
            housefinal = '2'
        elif house == '3':
            housefinal = '3'
        elif house == '4':
            housefinal = None
        else:
            await ctx.send("Invalid choice. Please try again.")
            return

        headers = mainHeader()  # Replace with your implementation of mainHeader()

        if housefinal:
            payload = {
                'house_id': housefinal
            }
            rep = requests.post("https://discord.com/api/v9/hypesquad/online", json=payload, headers=headers)
            if rep.status_code == 204:
                await ctx.send("Joined the selected HypeSquad house.")
            else:
                await ctx.send("Failed to join the HypeSquad house.")
        else:
            payload = {
                'house_id': housefinal
            }
            req = requests.delete('https://discord.com/api/v9/hypesquad/online', headers=headers, json=payload)
            if req.status_code == 204:
                await ctx.send("Left the HypeSquad.")
            else:
                await ctx.send("Failed to leave the HypeSquad.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")
# Send Avatars
@bot.command()
async def send_avatars(ctx):
    avatars_folder = "avatars" 

    supported_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    avatars = [
        file for file in os.listdir(avatars_folder)
        if os.path.isfile(os.path.join(avatars_folder, file))
        and os.path.splitext(file)[1].lower() in supported_extensions
    ]

    if not avatars:
        await ctx.send("No avatars found.")
        return

    sent_avatars = set()

    for avatar_file in avatars:
        try:
            if avatar_file in sent_avatars:
                continue

            avatar_path = os.path.join(avatars_folder, avatar_file)
            avatar = discord.File(avatar_path, filename=avatar_file)
            message = await ctx.send(file=avatar)

            sent_avatars.add(avatar_file)

            emoji = "<a:b_:1107465425031282698>"
            await message.add_reaction(emoji)
        except ValueError:
            continue

    await ctx.send("All avatars sent.")
# Send Animated Avatars",
@bot.command()
async def send_animated_avatars(ctx):
    avatars_folder = "a_avatars"  

    supported_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    avatars = [
        file for file in os.listdir(avatars_folder)
        if os.path.isfile(os.path.join(avatars_folder, file))
        and os.path.splitext(file)[1].lower() in supported_extensions
    ]

    if not avatars:
        await ctx.send("No avatars found.")
        return

    sent_avatars = set()

    for avatar_file in avatars:
        try:
            if avatar_file in sent_avatars:
                continue

            avatar_path = os.path.join(avatars_folder, avatar_file)
            avatar = discord.File(avatar_path, filename=avatar_file)
            message = await ctx.send(file=avatar)

            sent_avatars.add(avatar_file)

            emoji = "<a:b_:1107465425031282698>"
            await message.add_reaction(emoji)
        except ValueError:
            continue

    await ctx.send("All avatars sent.")
# Send Banners
@bot.command()
async def send_banners(ctx):
    avatars_folder = "banners"  

    supported_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    avatars = [
        file for file in os.listdir(avatars_folder)
        if os.path.isfile(os.path.join(avatars_folder, file))
        and os.path.splitext(file)[1].lower() in supported_extensions
    ]

    if not avatars:
        await ctx.send("No banner found.")
        return

    sent_avatars = set()

    for avatar_file in avatars:
        try:
            if avatar_file in sent_avatars:
                continue

            avatar_path = os.path.join(avatars_folder, avatar_file)
            avatar = discord.File(avatar_path, filename=avatar_file)
            message = await ctx.send(file=avatar)

            sent_avatars.add(avatar_file)

            emoji = "<a:b_:1107465425031282698>"
            await message.add_reaction(emoji)
        except ValueError:
            continue

    await ctx.send("All banner sent.")
# Link To File
@bot.command()
async def link(ctx, channel_id):
    if not isinstance(ctx.channel, discord.TextChannel):
        return await ctx.send("This command can only be used in a text channel.")

    target_channel = bot.get_channel(int(channel_id))

    if not target_channel:
        return await ctx.send("Invalid target channel.")

    await ctx.send("Send bulk links.")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        user_response = await bot.wait_for('message', check=check, timeout=60)

        video_links = user_response.content.split()

        if not video_links:
            return await ctx.send("No video links provided.")

        for video_link in video_links:
            async with aiohttp.ClientSession() as session:
                async with session.get(video_link) as response:
                    if response.status == 200:
                        video_content = await response.read()

                        file_name = video_link.split('/')[-1].replace('\x00', '')  

                        with open(file_name, 'wb') as file:
                            file.write(video_content)

                        file = discord.File(file_name)

                        await target_channel.send(file=file)

                        await asyncio.sleep(1)  
                        await asyncio.to_thread(lambda: remove_file(file_name))
                    else:
                        await ctx.send(f"Failed to download video from {video_link}")

        await ctx.send("Videos uploaded successfully.")
    except asyncio.TimeoutError:
        await ctx.send("Timed out. No video links were provided.")

def remove_file(file_name):
    os.remove(file_name)

# ASCII
@bot.command()
async def asci(ctx, *, text):
    await ctx.message.delete()
    f = Figlet(font='standard')
    ascii_art = f.renderText(text)
    await ctx.send(f'```{ascii_art}```')




bot.run(token)
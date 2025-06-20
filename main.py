import discord
from discord.ext import tasks
import aioconsole

client = discord.Client(intents=discord.Intents.all())
cmd_list = ["help", "guilds", "channels ", "members ",]
colors = {"reset": "\033[0m", "blue": "\033[94m", "green": "\033[92m", "red": "\033[91m", "yellow": "\033[93m", "purple": "\033[95m", "cyan": "\033[96m"}

def colorful_print(raw_text:str, *text_with_color:str, color:str|list="blue"):
    """Prints text in a colorful format."""
    if isinstance(color, str):
        for target_text in text_with_color:
            raw_text = raw_text.replace("{}", f"{colors[color]}{target_text}{colors['reset']}", 1)
    elif isinstance(color, list):
        for i, target_text in enumerate(text_with_color):
            raw_text = raw_text.replace("{}", f"{colors[color[i]]}{target_text}{colors['reset']}", 1)
    print(raw_text)

@tasks.loop()
async def cli():
    cmd = await aioconsole.ainput(">>> ")
    if cmd == "exit":
        await client.close()
    elif cmd == "" or cmd == cmd_list[0]:
        print("Available commands:")
        for command in cmd_list:
            colorful_print("- {}", command)
    # Get guilds info
    elif cmd == cmd_list[1]:
        print("Connected guilds:")
        for guild in client.guilds:
            colorful_print("{} (ID: {}) - Members: {}", guild.name, guild.id, guild.member_count, color=["yellow", "blue", "green"])
    # Get channels info for a specific guild
    elif cmd.startswith(cmd_list[2]):
        guild_id = cmd.split(" ")[1]
        guild = await client.fetch_guild(int(guild_id))
        if guild:
            channels = await guild.fetch_channels()
            print(f"Channels in guild {guild.name} (ID: {guild.id}):")
            for channel in channels:
                colorful_print("{} (ID: {}) - Type: {}", channel.name, channel.id, channel.type, color=["cyan", "blue", "yellow" if channel.type == discord.ChannelType.text else "purple"])
        else:
            print(f"Guild with ID {guild_id} not found.")
    # Get members info for a specific guild
    elif cmd.startswith(cmd_list[3]):
        guild_id = cmd.split(" ")[1]
        guild = await client.fetch_guild(int(guild_id))
        if guild:
            members = guild.fetch_members()
            print(f"Members in guild {guild.name} (ID: {guild.id}):")
            async for member in members:
                colorful_print("{} (ID: {}) - Status: {}", member.name, member.id, member.status, color=["green", "blue", "green" if member.status == discord.Status.online else "red"])
        else:
            print(f"Guild with ID {guild_id} not found.")
    # Get messages from a specific channel
    elif cmd.startswith("messages "):
        parts = cmd.split(" ")
        if len(parts) < 3:
            print("Usage: messages <guild_id> <channel_id>")
            return
        guild_id = parts[1]
        channel_id = parts[2]
        limit = 10 if len(parts) < 4 else int(parts[3])
        guild = await client.fetch_guild(int(guild_id))
        if guild:
            channel = await guild.fetch_channel(int(channel_id))
            if channel:
                messages = channel.history(limit=limit)
                print(f"Last {limit} messages in {channel.name} (ID: {channel.id}):")
                async for message in messages:
                    colorful_print("{}: {} ({})", message.author.name, message.content, message.created_at.strftime("%Y-%m-%d %H:%M:%S"), color=["blue", "green", "yellow"])
            else:
                print(f"Channel with ID {channel_id} not found in guild {guild.name}.")
        else:
            print(f"Guild with ID {guild_id} not found.")
    else:
        print("Unknown command")

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} (ID: {client.user.id})")
    print("Getting joined guilds...")
    for guild in client.guilds:
        colorful_print("{} (ID: {}) - Members: {}", guild.name, guild.id, guild.member_count, color=["yellow", "blue", "green"])
    cli.start()

client.run(input("Token: "))
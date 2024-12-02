# Import libraries
import os
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands
from ec2_metadata import ec2_metadata

###########

# Import environment variables
load_dotenv("token.env")

# Initializing environment variable token
token = os.getenv('TOKEN')

# Initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for commands and message content handling

#Recieving EC2 metadata
region = None
availability_zone = None
ip_address = None
try:
    ip_address = ec2_metadata.public_ipv4 or ec2_metadata.private_ipv4
    region = ec2_metadata.region
    availability_zone = ec2_metadata.availability_zone
except Exception as e:
    ip_address = "ip"
    region = "region"
    availability_zone = "zone"

#Initialize Dicord Client
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=intents)


#Display event handler when the bot is ready
@client.event 
async def on_ready(): 
	print("Logged in as a bot {0.user}".format(client))
	print(f'Your EC2 Data are as follows: IP Address: {ip_address}, Region: {region}, Availability Zone: {availability_zone}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Extract details from the message
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content).lower()

    print(f'Message "{user_message}" by {username} on {channel}')

    # Channel-specific message handling
    if channel in ["random", "bottombot"]:
        if user_message in ["hello", "hi"]:
            await message.channel.send(f'Hello {username}')
            return

        elif user_message == "bye":
            await message.channel.send(f'Bye {username}')
            return

        elif user_message == "tell me a joke":
            jokes = [
                "Can someone please shed more light on how my lamp got stolen?",
                "Why is she called Ilene? She stands on equal legs.",
                "What do you call a gazelle in a lion's territory? Denzel."
            ]
            await message.channel.send(random.choice(jokes))
            return

        elif user_message == "ip":
            await message.channel.send(f'Your public IP is {ip_address}')
            return

        elif user_message == "zone":
            await message.channel.send(f'Your availability zone is {availability_zone}')
            return

        elif user_message == "tell me about my server":
            await message.channel.send(
                f'Your EC2 region is {region}, Your public IP is {ip_address}, '
                f'Your availability zone is {availability_zone}'
            )
            return

#Define command to respond to "ping"
@client.command() 
async def ping(ctx): 
    await ctx.send('Pong!') 

# Running the bot
client.run(token)
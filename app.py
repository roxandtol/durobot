import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import os.path
import csv
import random
import hashlib
import json

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'

intents = discord.Intents.default()
intents.members = True  # Required to access member information
intents.message_content = True  # Required for message content
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='durosave')
async def durosave(ctx):
    await save_image(ctx, folder_name='temp', marker='0')

@bot.command(name='duro')
async def duro(ctx):
    await send_random_image(ctx, marker='0')

@bot.command(name='lmaosave')
async def lmaosave(ctx):
    await save_image(ctx, folder_name='temp', marker='1')

@bot.command(name='lmao')
async def lmao(ctx):
    await send_random_image(ctx, marker='1')

@bot.command(name='durumsave')
async def lmaosave(ctx):
    await save_image(ctx, folder_name='temp', marker='2')

@bot.command(name='durum')
async def lmao(ctx):
    await send_random_image(ctx, marker='2')


async def read_error_message(kind, ctx):
    guild_id = str(ctx.guild.id)
    json_filename = f'server_configs/{guild_id}.json'
    if not os.path.exists("server_configs"):
        os.makedirs("server_configs")

    try:
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # If the file does not exist, create it with default data
        data = {
            "duped_file": ["gilipollas, esto ya se ha subido"],
            "uploaded_file": ["gracias por la fotopolla"],
            "no_file_uploaded": ["pero sube algo, masón de mierda"],
            "no_images": ["No hay cosas duras, f"]
        }
        with open(json_filename, 'w') as new_json_file:
            json.dump(data, new_json_file, indent=4)

    if kind in data:
        if data[kind]:
            # Return a random element from the specified array
            return random.choice(data[kind])
        else:
            raise NothingInArray ("There's nothing in the array")
    else:
        raise NothingInArray ("There's nothing in the array")
    
async def save_image(ctx, folder_name, marker):
    # Check if the command has an attachment
    if len(ctx.message.attachments) == 0:
        no_file_uploaded = read_error_message("no_file_uploaded", ctx)
        await ctx.send(f"{no_file_uploaded}")
        return
    attachment = ctx.message.attachments[0]
    attachment_url = attachment.url
    username = ctx.author.name

    guild_id = str(ctx.guild.id)
    server_lists = 'server_lists'
    filename = f'server_lists/{guild_id}.csv'
    temp_folder = folder_name
    
    duped_file = read_error_message("duped_file", ctx)
    uploaded_file = read_error_message("uploaded_file", ctx)
    
    # Create the temp folder if it doesn't exist
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Create {guild_id}.csv if not exists
    if not os.path.exists(filename):
        open(filename, 'w').close()

    # Save the attachment to the temp folder
    file_path = os.path.join(temp_folder, f'temp.{attachment.filename.split(".")[-1]}')
    await attachment.save(file_path)

    # Calculate SHA256 hash of the saved file
    hash_object = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_object.update(chunk)
    file_hash = hash_object.hexdigest()

    # Check if the hash already exists in the CSV file
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        existing_hashes = [row[2] for row in csv_reader]

    if file_hash in existing_hashes:
        os.remove(file_path)  # Remove the duplicate file
        await ctx.send(f"{duped_file}")
        return

    # Save attachment link, username, hash, and marker to the CSV file
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([attachment_url, username, file_hash, marker])

    await ctx.send(f"{uploaded_file}")

async def send_random_image(ctx, marker):
    guild_id = str(ctx.guild.id)
    filename = f'server_lists/{guild_id}.csv'
    
    no_images = read_error_message("no_images", ctx)

    # Read all attachment links and hashes from the CSV file
    try:
        with open(filename, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            duro_data = [(row[0], row[1], row[2]) for row in csv_reader if row[3] == marker]

        # Get a random attachment link
        if duro_data:
            random_duro = random.choice(duro_data)
            await ctx.send(f"{random_duro[0]}")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        await ctx.send(f"{no_images}")

bot.run(TOKEN)
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
intents.message_content = True  # Required for message content
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='duro')
async def duro(ctx):
    await send_random_image(ctx, marker='0')

@bot.command(name='lmao')
async def lmao(ctx):
    await send_random_image(ctx, marker='1')

@bot.command(name='durum')
async def lmao(ctx):
    await send_random_image(ctx, marker='2')
    
@bot.command(name='durosave')
async def durosave(ctx):
    await save_image(ctx, folder_name='temp', marker='0', save_to_public=False)

@bot.command(name='lmaosave')
async def lmaosave(ctx):
    await save_image(ctx, folder_name='temp', marker='1', save_to_public=False)

@bot.command(name='durumsave')
async def durumsave(ctx):
    await save_image(ctx, folder_name='temp', marker='2', save_to_public=True)
    
async def update_recent_attachment(json_filename, attachment_url):
    # Load JSON data
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
    
    # Add attachment URL to the recent list
    data["recent"].append(attachment_url)
    
    # Remove the first attachment URL if there are more than the specified amount in the json in the recent list
    max_data = data["recent_amount"]
    
    if len(data["recent"]) > max_data:
        data["recent"].pop(0)
    
    # Write updated data back to JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

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
            "duped_file": ["Esto ya se ha subido"],
            "uploaded_file": ["Gracias por la foto"],
            "no_file_uploaded": ["No has subido nada"],
            "no_images": ["No hay cosas duras, f"],
            "public_images": [True],
            "recent_amount": 10,
            "recent": []
        }
        with open(json_filename, 'w') as new_json_file:
            json.dump(data, new_json_file, indent=4)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON in {json_filename}. {str(e)}")

    if kind in data:
        if data[kind]:
            # Return a random element from the specified array
            return random.choice(data[kind])
        else:
            raise NothingInArray("There's nothing in the array")
    else:
        raise NothingInArray("There's nothing in the array")

async def save_image(ctx, folder_name, marker, save_to_public):
    # Check if the command has an attachment
    if len(ctx.message.attachments) == 0:
        no_file_uploaded = await read_error_message("no_file_uploaded", ctx)
        await ctx.send(f"{no_file_uploaded}")
        return

    attachment = ctx.message.attachments[0]
    attachment_url = attachment.url
    username = ctx.author.name

    guild_id = str(ctx.guild.id)
    server_lists = 'server_lists'
    filename = f'server_lists/{guild_id}.csv'
    temp_folder = folder_name

    duped_file = await read_error_message("duped_file", ctx)
    uploaded_file = await read_error_message("uploaded_file", ctx)

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

    # Save attachment link, username, hash, and marker to the appropriate CSV file
    if save_to_public:
        csv_filename = 'public.csv'
    else:
        csv_filename = f'server_lists/{guild_id}.csv'

    with open(csv_filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([attachment_url, username, file_hash, marker])
    
    # Update the recent attachment in the JSON file
    json_filename = f'server_configs/{guild_id}.json'
    await update_recent_attachment(json_filename, attachment_url)

    await ctx.send(f"{uploaded_file}")

async def send_random_image(ctx, marker):
    guild_id = str(ctx.guild.id)
    guild_filename = f'server_lists/{guild_id}.csv'
    public_filename = 'public.csv'

    no_images = await read_error_message("no_images", ctx)

    try:
        if await read_error_message("public_images", ctx):
            with open(public_filename, 'r', newline='') as public_csv:
                public_reader = csv.reader(public_csv)
                public_data = [(row[0], row[1], row[2]) for row in public_reader if row[3] == marker]
        else:
            public_data = []

        # Check guild-specific CSV only if it exists
        if os.path.exists(guild_filename):
            with open(guild_filename, 'r', newline='') as guild_csv:
                guild_reader = csv.reader(guild_csv)
                guild_data = [(row[0], row[1], row[2]) for row in guild_reader if row[3] == marker]
        else:
            guild_data = []

        # Combine guild-specific and public data
        combined_data = guild_data + public_data
        
        # Filter out attachments that are in the recent list
        json_filename = f'server_configs/{guild_id}.json'
        with open(json_filename, 'r') as json_file:
            recent_attachments = json.load(json_file)["recent"]
        
        combined_data = [data for data in combined_data if data[0] not in recent_attachments]

        # Get a random attachment link
        if combined_data:
            random_duro = random.choice(combined_data)
            await ctx.send(f"{random_duro[0]}")
            # Update the recent attachment in the JSON file
            await update_recent_attachment(json_filename, random_duro[0])
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        await ctx.send(f"{no_images}")

bot.run(TOKEN)
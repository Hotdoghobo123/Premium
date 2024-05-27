import discord
from discord.ext import commands
import random
import asyncio

# Replace with your actual bot token
TOKEN = 'MTI0NDcwMzY1OTcyODgzNDY0MA.GziSQL.GvpZWHpfgjkhn9PL_seCZQ44ujNGvR1Y--Dt6A'

# Define the allowed channel ID
ALLOWED_CHANNEL_ID = '1244693549308444763'

# URLs of the coin flip GIFs
HEADS_GIF_URL = 'https://media1.tenor.com/m/nEu74vu_sT4AAAAC/heads-coinflip.gif'  # Replace with your preferred Heads GIF URL
TAILS_GIF_URL = 'https://media1.tenor.com/m/kK8D7hQXX5wAAAAC/coins-tails.gif'      # Replace with your preferred Tails GIF URL

# Initialize the bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# List to store the history of flips
flip_history = []

# Custom prediction pattern
custom_pattern = ['heads', 'tails', 'heads', 'heads', 'tails', 'tails']

# Function to predict the next flip based on the custom pattern
def predict_next_flip():
    if len(flip_history) < len(custom_pattern):
        return random.choice(['heads', 'tails'])
    else:
        index = len(flip_history) % len(custom_pattern)
        return custom_pattern[index]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def send_flip_result(ctx, result):
    gif_url = HEADS_GIF_URL if result == 'heads' else TAILS_GIF_URL
    embed = discord.Embed(title="Flipping the coin...", color=discord.Color.blue())
    embed.set_image(url=gif_url)
    embed.set_thumbnail(url=gif_url)  # Set the thumbnail
    message = await ctx.send(embed=embed)
    await asyncio.sleep(3)  # Wait for the duration of the GIF
    embed.title = f"The coin landed on: **{result.capitalize()}**"
    await message.edit(embed=embed)

@bot.command(name='bloxybetH')
async def bloxybet_heads(ctx):
    prediction = predict_next_flip()
    flip_history.append(prediction)
    await send_flip_result(ctx, prediction)
    await ctx.send("We recommend canceling if your flip lasts more than 5 seconds.")

@bot.command(name='bloxybetT')
async def bloxybet_tails(ctx):
    prediction = predict_next_flip()
    flip_history.append(prediction)
    await send_flip_result(ctx, prediction)
    await ctx.send("We recommend canceling if your flip lasts more than 5 seconds.")

@bot.command(name='commands')
async def commands_list(ctx):
    command_list = [
        "```",
        "Available Commands:",
        "!bloxybetH - Predicts the next coin flip for BloxyBet (Heads).",
        "!bloxybetT - Predicts the next coin flip for BloxyBet (Tails).",
        "!history - Shows the history of flips.",
        "!unrig - Resets the prediction counts and flip history.",
        "!commands - Shows this list of commands.",
        "```"
    ]
    await ctx.send("\n".join(command_list))

@bot.command(name='history')
async def show_history(ctx):
    if not flip_history:
        await ctx.send("No flips yet.")
        return

    history_message = "```"
    for index, flip in enumerate(flip_history, start=1):
        history_message += f"{index}. {flip}\n"
    history_message += "```"
    await ctx.send(history_message)

@bot.command(name='unrig')
async def unrig(ctx):
    global flip_history
    flip_history = []
    await ctx.send("Prediction counts and flip history have been reset.")






bot.run(TOKEN)

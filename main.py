import os
import logging
import discord
from discord.ext import commands
from datetime import datetime, timezone
from dotenv import load_dotenv
from utils import load_config

config = load_config()

print(discord.__version__)
load_dotenv()
log_path='./logs'
os.makedirs(log_path,exist_ok=True)
token = os.getenv("BOT_TOKEN")

file_name = datetime.now(timezone.utc).strftime('%Y-%m_error.log')
log_files = logging.FileHandler(filename='logs/'+ file_name, encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    command_prefix=config['prefix'], 
    intents=intents, 
    case_insensitive=True
    )

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            ext_name = f'cogs.{filename[:-3]}'
            if ext_name in bot.extensions:
                await bot.reload_extension(ext_name)
            else:
                await bot.load_extension(ext_name)

async def setup_hook(self):
    await self.load_extension("cogs.help")

@bot.event
async def on_ready():
    await load_cogs()
    
@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    """Reload all cogs when the code has changed."""
    await load_cogs()
    await ctx.send("Reload all done.")

bot.run(token, log_handler=log_files)
import aiohttp
import discord, os
from discord.ext import commands
from dotenv import load_dotenv
import logging


load_dotenv()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
prefix = ["."]

os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix = prefix, 
                        case_insensitive = True, 
                        trip_after_prefix=True,
                        intents=discord.Intents.all(), 
                        owner_ids = [675104167345258506, 787707616205340702, 815973091208986705])

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} has been loaded!")

    async def on_ready(self):
        guild = self.get_guild(1045853815699668993)
        await self.change_presence(status = discord.Status.idle, activity=discord.Activity(name=guild.name, type=discord.ActivityType.watching))
        print(self.user.id)

if __name__ == '__main__':
    intents = discord.Intents.all()
    bot = Bot(intents=intents)
    bot.run(os.getenv('TOKEN'))
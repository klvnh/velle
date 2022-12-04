import discord
from discord.ext import commands
from scaper.icon_scraper import IconScraper
import re
from converters import CustomConverters


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def output(self, url: str):
        data = await self.bot.session.get(url)
        return await data.json()

    @commands.hybrid_command(brief='Velle will share her latency!')
    async def ping(self, ctx):
        await ctx.reply(f'Pong! {round(self.bot.latency * 1000)}MS', mention_author=False)

    @commands.hybrid_command(brief='Velle will return the targetted member\'s avatar!')
    async def pfp(self, ctx, user : discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title=f'{user.name}\'s avatar', color=0x2F3136)
        embed.set_image(url=user.display_avatar.url)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name='pscrape', brief='Velle will return the image of the given pinterest link!')
    async def pinterest_scrape(self, ctx, urls : commands.Greedy[CustomConverters]):
        paginator = commands.Paginator(prefix='', suffix='')
        scraper = IconScraper(self.bot)
        for results in urls:
            url = await scraper.pinterest(results)
            paginator.add_line(url[0])
        for page in paginator.pages:
            await ctx.send(page)

async def setup(bot):
    await bot.add_cog(Fun(bot))
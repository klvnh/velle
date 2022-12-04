import discord
from discord.ext import commands
import traceback

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(brief='Enables slash commands.')
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.message.add_reaction('\U0001f375')

    @commands.hybrid_command(brief='Reloads all the categories.')
    async def reload(self, ctx):
        paginator = commands.Paginator(prefix='', suffix='')
        for extension in list(self.bot.extensions.keys()):
            try:
                await self.bot.reload_extension(extension)
                paginator.add_line(f"> Succesfully reloaded: ``{extension}``")
            except Exception as e:
                er = getattr(e, 'original', e)
                paginator.add_line(f'\U0001f6ab Failed to load extension: ``{extension}``')
                error = ''.join(traceback.format_exception(type(er), er, er.__traceback__))
                paginator.add_line('`'*3 + f'\n{error}' + '`'*3)

        for page in paginator.pages:
            await ctx.send(page, delete_after=5)
            await ctx.message.add_reaction('\U0001f375')

    @commands.hybrid_group(brief='Velle will edit the server!')
    async def guild_edit(self, ctx):
        await ctx.reply("A place holder since discord slash commands can't run this!", mention_author=False)

    @guild_edit.command(brief='Velle will edit the server icon!')
    async def icon(self, ctx, image_url : str):
        icon = await self.bot.session.get(image_url)
        image_bytes = await icon.read()
        await ctx.guild.edit(icon=image_bytes)
        await ctx.reply('Velle just updated the server icon!')

    @guild_edit.command(brief='Velle will edit the server banner!')
    async def banner(self, ctx, image_url : str):
        icon = await self.bot.session.get(image_url)
        image_bytes = await icon.read()
        await ctx.guild.edit(banner=image_bytes)
        await ctx.reply('Velle just updated the server banner!')

    @guild_edit.command(brief='Velle will edit the server vanity code!')
    async def vanity(self, ctx, code : str):
        await ctx.guild.edit(vanity_code=code)
        await ctx.reply('Velle just updated the server vanity link!')

    @commands.hybrid_command(brief='Velle will return the number of invites on the server vanity!')
    async def vanity_invite(self, ctx):
        vanity_url = await ctx.guild.vanity_invite()
        uses = vanity_url.uses
        await ctx.reply(f'The vanity code: ``discord.gg/{vanity_url.code}`` has {uses} invites!', mention_author=False)
    
async def setup(bot):
    await bot.add_cog(Owner(bot))
    
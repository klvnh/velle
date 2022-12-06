import discord
from discord.ext import commands
import traceback
import json

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

    @commands.hybrid_command()
    async def create_embed(self, ctx):
        embed = discord.Embed(title='Default', description='Default response.')
        with open("embed.json", "w") as outfile:
            json.dump(embed.to_dict(), outfile)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def create_embed(self, ctx):
        embed = discord.Embed(title='Default', description='Defautlt response.')
        with open('embed.json', 'w') as outfile:
            data = json.load(outfile)
            json.dump(data, outfile)
            await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def show_embed(self, ctx):
        with open('embed.json', "r") as outfile:
            data = json.load(outfile)
        await ctx.send(embed=discord.Embed.from_dict(data))

    @commands.hybrid_group()
    async def embed_edit(self, ctx):
        await ctx.reply("A place holder since discord slash commands can't run this!", mention_author=False)

    @embed_edit.command()
    async def title(self, ctx, *, title):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['title'] = title
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @embed_edit.command()
    async def description(self, ctx, *, description):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['description'] = description
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @embed_edit.command()
    async def image(self, ctx, *, url : str):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['image'] = {'url': url}
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @embed_edit.command()
    async def thumbnail(self, ctx, *, url : str):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['thumbnail'] = {'url': url}
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @embed_edit.command()
    async def color(self, ctx, *, color : int):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['color'] = color
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @embed_edit.command()
    async def footer_text(self, ctx, *, text):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['footer'] = {'text': text}
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @embed_edit.command()
    async def footer_icon(self, ctx, *, icon_url):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data['footer'] = {'icon_url': icon_url}
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))

    @commands.hybrid_command()
    async def embed_remove(self, ctx, part):
        with open('embed.json', "r+") as outfile:
            data = json.load(outfile)
            data.pop(part)
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
        await ctx.send(embed=discord.Embed.from_dict(data))
    
    
async def setup(bot):
    await bot.add_cog(Owner(bot))
    
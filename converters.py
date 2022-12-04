from discord.ext import commands

class CustomConverters(commands.Converter):
    async def convert(self, ctx, urls):
        return str(urls)
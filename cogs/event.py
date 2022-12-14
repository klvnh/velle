import discord
from discord.ext import commands
import json
import traceback
import sys
import tagformatter

parser = tagformatter.Parser()
@parser.tag("user")
def member(env):
    return env.user.mention

@parser.tag("member_count")
def member_count(env):
    return env.guild.member_count

@parser.tag("guild")
def guild(env):
    return env.guild.name

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = {}
    
    @commands.Cog.listener('on_command_error')
    async def error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener('on_presence_update')
    async def vanity(self, before: discord.Member, after: discord.Member) -> None:
        vanity = ['gg/velle', '.gg/velle', '/velle']
        after_status: discord.CustomActivity = discord.utils.find(lambda a: isinstance(a, discord.CustomActivity), after.activities) 
        before_status: discord.CustomActivity = discord.utils.find(lambda a: isinstance(a, discord.CustomActivity), before.activities) 
        before_actvity: discord.Activity = discord.utils.find(lambda a: isinstance(a, discord.Activity), before.activities)
        after_activity: discord.Activity = discord.utils.find(lambda a: isinstance(a, discord.Activity), after.activities)
        before_vanity_in_status = any(word in str(before_status).lower() for word in vanity)
        after_vanity_in_status = any(word in str(after_status).lower() for word in vanity)
        does_user_have_role = any(role for role in after.roles if role.id == 1046497852223926457)
        inbox: discord.TextChannel = self.bot.get_channel(1046498784529625099)

        if does_user_have_role and after_vanity_in_status:
            return

        if after.status == discord.Status.offline and does_user_have_role:
            return

        if before_vanity_in_status and after_vanity_in_status:
            return

        if after_vanity_in_status and not does_user_have_role:
            format = ' or '.join(vanity)
            await after.add_roles(discord.Object(1046497852223926457))
            embed = discord.Embed(description=f'``???`` {after.mention} you got <@&1046497852223926457> role!', color=0x2F3136)
            embed.set_footer(text=f'put {format} in your status')
            await inbox.send(embed=embed)

        if not after_vanity_in_status and does_user_have_role:
            after.status in (discord.Status.dnd, discord.Status.online, discord.Status.idle)
            await after.remove_roles(discord.Object(1046497852223926457))         

    @commands.Cog.listener('on_member_join')
    async def welcome(self, member):
        gen = self.bot.get_channel(1045853816320430143)
        if member.bot:
            return
        else:
            parsing = ['title', 'description']
            with open('embed.json', "r") as outfile:
                data = json.load(outfile)
                for p in parsing:
                    try:
                        parsed = parser.parse(data[p], env={"user": member, "guild": member.guild})
                        data[p] = parsed
                    except:
                        pass
                footer = parser.parse(data['footer']['text'], env={"user": member, "guild": member.guild})
                data['footer']['text'] = footer
                await gen.send(f'{member.mention}', embed=discord.Embed.from_dict(data))

async def setup(bot):
    await bot.add_cog(Event(bot))
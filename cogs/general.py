import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self,ctx):
         """Send a message to the user."""
         await ctx.send(f'Hello {ctx.author.mention}!')

    @commands.command()
    async def ping(self,ctx):
        """check bot delay"""
        ping = round(self.bot.latency*1000)
        if ping<=80:
            color = discord.Color.green()
            description = 'Very good'
        elif ping<=150:
            color = discord.Color.yellow()
            description = 'Good'
        elif ping<=250:
            color = discord.Color.orange()
            description = 'Ok'
        elif ping<=800:
            color = discord.Color.red()
            description = 'High'
        else:
            color = discord.Color.dark_red()
            description = 'Very High'

        embed=discord.Embed(
            title="Ping",
            description=description,
            color=color
        )
        embed.add_field(name='Delay', value=f'{ping}ms' , inline=False)
        await ctx.send(embed=embed)
             
    @commands.command()
    async def userinfo(self,ctx, member:discord.Member = None):
        """Display user information detail"""
        await ctx.message.delete()
        embed = discord.Embed(
            title=f'User Info',
            color=discord.Color.random()
        )
        member = member or ctx.author
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name='Name / ID', value=f'{member.mention} ({member.id})', inline=False)
        embed.add_field(name='Highest Role', value=member.top_role.mention, inline=True)
        embed.add_field(name='Bot or Human', value='Bot' if member.bot else  'Human' , inline=True)
        embed.add_field(name='Server Booster', value=member.premium_since.strftime("%Y-%m-%d %H:%M:%S") if member.premium_since else 'None' , inline=False)
        embed.add_field(name='Joined Server', value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name='Account Created', value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text=f'Search By {ctx.author}',icon_url=f'{ctx.author.display_avatar.url}')
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self,ctx):
        """Display current server information detail"""
        await ctx.message.delete()
        guild = ctx.guild
        embed = discord.Embed(
             title=f'Server Info',
             color=discord.Color.random()
        )

        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name='Name / ID', value=f'{guild} ({guild.id})', inline=True)
        embed.add_field(name='Owner', value=guild.owner.mention, inline=False)
        embed.add_field(name='Member Count', value=guild.member_count, inline=False)
        embed.add_field(name='Server Created', value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text=f'Search By {ctx.author}',icon_url=f'{ctx.author.display_avatar.url}')
        await ctx.send(embed=embed)
                   
async def setup(bot):
    await bot.add_cog(General(bot))
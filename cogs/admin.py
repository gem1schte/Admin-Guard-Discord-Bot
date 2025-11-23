import discord
import asyncio
import datetime
from discord.ext import commands
from utils import load_config
from utils import now_utc

config = load_config()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """Shut down the bot."""
        await ctx.bot.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member:discord.Member, *, reason=None):
        """Mute a member by assigning the mute role."""
        await ctx.message.delete()
        mute_role = discord.utils.get(ctx.guild.roles, name = config['mute-role'])

        if not mute_role:
            mute_role = await ctx.guild.create_role(name = config['mute-role'])

            for channel in ctx.guild.channels:
                await channel.set_permissions(
                    mute_role,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=True
                    )

        if mute_role in member.roles:
            return await ctx.send(f'{member.mention} this user has been mute.')
        
        await member.add_roles(mute_role,reason=reason)
        embed = discord.Embed(
            title="Muted",
            color=discord.Color.red()
        )
        embed.add_field(name='User',value = f'{member.mention} ({member.id})',inline=False)
        embed.add_field(name='From',value = f'{ctx.author.mention} ({ctx.author.id})',inline=False)
        embed.add_field(name='Reason',value = reason,inline=False)
        embed.set_footer(text=now_utc())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def timeout(self, ctx, member: discord.Member, time: str, *, reason=None):
        """Apply a timeout to a member using s/m/h/d units."""
        await ctx.message.delete()
        unit = time[-1] # Get the last character of the string (s/m/h/d)
        value = time[:-1] # Get all characters except the last one
        value = int(value)

        if unit == "s":
            seconds = value
        elif unit =="m":
            seconds = value * 60
        elif unit =="h":
            seconds = value * 3600
        elif unit =="d":
            seconds = value * 86400
            
        until = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
        await member.timeout(until,reason=reason)

        embed = discord.Embed(
            title=f'Timeout',
            color=discord.Color.red()
        )
        embed.add_field(name='User',value = f'{member.mention} ({member.id})',inline=False)
        embed.add_field(name='From',value = f'{ctx.author.mention} ({ctx.author.id})',inline=False)
        embed.add_field(name='Time',value = f'{value}{unit}' ,inline=False)
        embed.add_field(name='Reason',value = reason,inline=False)
        embed.set_footer(text=now_utc())
        await ctx.send(embed=embed)

        await asyncio.sleep(seconds)
        await member.timeout(None)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member:discord.Member, *, reason=None):
        """Remove the mute role from a member."""
        await ctx.message.delete()
        mute_role = discord.utils.get(ctx.guild.roles, name = config['mute-role'])

        if mute_role not in member.roles:
            return await ctx.send(f'{member.mention} this user is not mute.')

        await member.remove_roles(mute_role,reason=reason)

        embed = discord.Embed(
            title="Unmuted",
            color=discord.Color.green()
        )
        embed.add_field(name='User',value = f'{member.mention} ({member.id})',inline=False)
        embed.add_field(name='From',value = f'{ctx.author.mention} ({ctx.author.id})',inline=False)
        embed.add_field(name='Reason',value = reason,inline=False)
        embed.set_footer(text=now_utc())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        """Kick a member from the server."""
        await ctx.message.delete()
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="Kicked",
            color=discord.Color.red()
        )
        embed.add_field(name='User',value = f'{member.mention} ({member.id})',inline=False)
        embed.add_field(name='From',value = f'{ctx.author.mention} ({ctx.author.id})',inline=False)
        embed.add_field(name='Reason',value = reason,inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member:discord.Member, *, reason=None):
        """Ban a member from the server."""
        await ctx.message.delete()
        await member.ban(reason=reason)
        
        embed = discord.Embed(
            title="Banned",
            color=discord.Color.red()
        )
        embed.add_field(name='User',value = f'{member.mention} ({member.id})',inline=False)
        embed.add_field(name='From',value = f'{ctx.author.mention} ({ctx.author.id})',inline=False)
        embed.add_field(name='Reason',value = reason,inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, user_id: int, *, reason=None):
        """Unban a user using their user ID."""
        await ctx.message.delete()

        user = None
        async for entry in ctx.guild.bans():
            if entry.user.id == user_id:
                user = entry.user
                break

        if user is None:             
            return await ctx.send("This user is not banned.")
                        
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(
            title="Unbaned",
            color=discord.Color.red()
        )
        embed.add_field(name='User',value = f'{user.mention} ({user.id})',inline=False)
        embed.add_field(name='From',value = f'{ctx.author.mention} ({ctx.author.id})',inline=False)
        embed.add_field(name='Reason',value = reason,inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self,ctx, *, message:str):
        """Send a message to the announcement channel."""
        await ctx.message.delete()
        announcement_channel = discord.utils.get(ctx.guild.text_channels,  name = config['announcement'])

        if not announcement_channel:
            announcement_channel = await ctx.guild.create_text_channel(name = config['announcement'])

            await announcement_channel.set_permissions(
                ctx.guild.default_role,
                send_messages=False,
                send_messages_in_threads=False
            )
        await announcement_channel.send(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self,ctx, amount:int):
        """Delete a specified number of messages from the current channel."""
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

async def setup(bot):
    await bot.add_cog(Admin(bot))
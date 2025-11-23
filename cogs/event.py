import os
import discord
from discord.ext import commands
from utils import load_config
from utils import now_utc

config = load_config()

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content == "test work":
            await message.channel.send("Bot working!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name = config['welcome-channel'])
        member_role =  discord.utils.get(member.guild.roles, name = config['member-role'])

        if not welcome_channel:
            welcome_channel = await member.guild.create_text_channel(name = config['welcome-channel'])

            await welcome_channel.set_permissions(
                member.guild.default_role,
                read_messages=True,
                send_messages=False,
                send_messages_in_threads=False,
                add_reactions=False
            )

        if not member_role:
            member_role = await member.guild.create_role(name = config['member-role'])

        if member_role:
            await member.add_roles(member_role)

        if welcome_channel:
            embed = discord.Embed(
                title="👋 Welcome!",
                description=f'{member.mention} welcome to the server！🎉',
                color=discord.Color.green()
                )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=now_utc())
            await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave_channel = discord.utils.get(member.guild.text_channels, name = config['leave-channel'])

        if not leave_channel:
            leave_channel = await member.guild.create_text_channel(name = config['leave-channel'])

        await leave_channel.set_permissions(
                member.guild.default_role,
                read_messages=True,
                send_messages=False,
                send_messages_in_threads=False,
                add_reactions=False
            )

        if leave_channel:
            embed = discord.Embed(
                title="👋 Goodbye!",
                description=f'{member.mention} leave the server',
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=now_utc())
            await leave_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        message_history_channel = discord.utils.get(before.guild.text_channels, name = config['history-channel'])
        member = before.author
        
        if not message_history_channel:
            message_history_channel = await member.guild.create_text_channel(name = config['history-channel'])

            await message_history_channel.set_permissions(
                before.guild.default_role,
                read_messages=False
            )

        embed = discord.Embed(
            title="Edited",
            color=discord.Color.red()
        )
        
        embed.add_field(name="User", value = f'{member.mention} ({member.id})',inline=True)
        embed.add_field(name="Previous message", value = before.content,inline=False)
        embed.add_field(name="New message", value = after.content,inline=False)
        embed.set_footer(text=now_utc())
        await message_history_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        message_history_channel = discord.utils.get(message.guild.text_channels, name = config['history-channel'])
        
        if not message_history_channel:
            message_history_channel = await message.guild.create_text_channel(name = config['history-channel'])

            await message_history_channel.set_permissions(
                message.guild.default_role,
                read_messages=False
            )
                   
        embed = discord.Embed(
            title="Deleted",
            color=discord.Color.red()
        )
        member = message.author
        embed.add_field(name="User", value = f'{member.mention} ({member.id})',inline=True)
        embed.add_field(name="Deleted message", value = message.content,inline=False)
        embed.set_footer(text=now_utc())
        await message_history_channel.send(embed=embed)
         
async def setup(bot):
    await bot.add_cog(Event(bot))
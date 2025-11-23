import discord
from discord.ext import commands

class Help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        # This method is called when the help command is invoked without arguments.
        # It should list all cogs and their general purpose.
        embed = discord.Embed(title="Bot Help", description="Here are the available commands, organized by category (Cog).")
        for cog, commands_list in mapping.items():
            if cog:
                cog_name = cog.qualified_name
                cog_description = cog.description if cog.description else "No description provided."
                embed.add_field(name=f"**{cog_name}**", value=f"{cog_description}\nCommands: {', '.join([c.name for c in commands_list])}", inline=False)
            else:
                # Handle commands not belonging to any cog (if any)
                pass # You can add specific handling here if needed
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        # This method is called when the help command is invoked with a command name.
        # It should provide detailed information about that specific command.
        embed = discord.Embed(
            title=f"Help for {self.context.prefix}{command.name}", 
            description=command.help if command.help else "No help available.",
            color=discord.Color.red()
            )
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
        if command.signature:
            embed.add_field(name="Usage", value=f"{self.context.prefix}{command.name} {command.signature}", inline=False)
        await self.get_destination().send(embed=embed)

async def setup(bot):
        bot.help_command = Help()
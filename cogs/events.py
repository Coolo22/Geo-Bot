
import discord 
import random

from discord.ext import commands as cmds
from resources import config, lang

from resources.interaction_templates import language, get_commands

class events(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cmds.Cog.listener()
    async def on_guild_join(self, guild : discord.Guild):
        print(guild.name)

        suitable_channel : discord.TextChannel = None 

        for channel in guild.text_channels:

            if "chat" in channel.name or "general" in channel.name or "commands" in channel.name or "lounge" in channel.name or "bot" in channel.name:
                suitable_channel = channel 
        
        if suitable_channel == None:
            suitable_channel = random.choice(guild.text_channels)
        
        embed = discord.Embed(title="Thanks for adding me!", description=f"The default language is **{lang.default.fullName}**. Change it with the select menu below.", color=config.embed)
        embed.add_field(name="Get started", value="Try some of my commands with:\n`/help commands` (or the button below)")
        
        
        view = discord.ui.View()
        view.add_item(language.LanguageSelector(self.bot))
        view.add_item(get_commands.GetCommandsButton(self.bot.client, lang.default))

        await suitable_channel.send(embed=embed, view=view)
    
def setup(bot):
    bot.add_cog(events(bot))
    
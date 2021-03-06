

import discord 

from resources import lang

class Options():

    def __init__(self, client):
        self.client = client 
    
    def get_guild(self, guild : discord.Guild):
        return GuildOptions(self, guild)
    
    def get_user(self, user : discord.User, language):
        return UserOptions(self, user, language)

class UserOptions():
    
    def __init__(self, options : Options, user : discord.User, language):
        self.user = user 
        self._options = options 
        self._language = language

        self.data = None 
        self.languageOverwrite = None

        self.language = None

        self._from_json(
            self._options.client.http.get_file_sync("data/options.json")
        )

        
    
    def _from_json(self, data : dict):
        self.data = data 

        self.languageOverwrite = None
        if "users" in data and str(self.user.id) in data["users"] and "languageOverwrite" in data["users"][str(self.user.id)]:
            self.languageOverwrite = data["users"][str(self.user.id)]["languageOverwrite"]

            for language in lang.supported_languages:
                if language.shortName == self.languageOverwrite:
                    self.languageOverwrite = language
        
        self.language = self.languageOverwrite or self._language
    
    def to_json(self):
        return {"languageOverwrite":self.languageOverwrite}

    async def save_json(self):
        dt = self._options.client.http.get_file_sync("data/options.json")

        if "users" not in dt:
            dt["users"] = {}

        dt["users"][str(self.user.id)] = self.to_json()
        return await self._options.client.http.save_to_file("data/options.json", dt)


class GuildOptions():

    def __init__(self, options : Options, guild : discord.Guild):
        self.guild = guild 
        self._options = options
        self.data = None

        self.language = None 
        self.multipleChoiceType = None

        self._from_json(
            self._options.client.http.get_file_sync("data/options.json")
        )
    
    
    
    async def init(self, interaction : discord.Interaction):
        if "guilds" not in self.data or str(interaction.guild.id) not in self.data["guilds"] or "language" not in self.data["guilds"][str(interaction.guild.id)]:
            
            self.language = lang.private_command(self._options.client, interaction).shortName 

            await self.save_json()

        return self.language
    
    def _from_json(self, data : dict):
        self.data = data 

        self.language = "en"
        if "guilds" in data and str(self.guild.id) in data["guilds"] and "language" in data["guilds"][str(self.guild.id)]:
            self.language = data["guilds"][str(self.guild.id)]["language"]
            
        self.multipleChoiceType = "button"
        if "guilds" in data and str(self.guild.id) in data["guilds"] and "multipleChoiceType" in data["guilds"][str(self.guild.id)]:
            self.multipleChoiceType = data["guilds"][str(self.guild.id)]["multipleChoiceType"]
    
    def to_json(self):
        return {"language":self.language, "multipleChoiceType":self.multipleChoiceType}

    async def save_json(self):
        dt = self._options.client.http.get_file_sync("data/options.json")

        if "guilds" not in dt:
            dt["guilds"] = {}

        dt["guilds"][str(self.guild.id)] = self.to_json()
        return await self._options.client.http.save_to_file("data/options.json", dt)

import discord
from discord.ext import commands
import json
import time
import sqlite3 as sl



#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]
prefix = configjson["prefix"]
dbpath = r"/Volumes/Pasghetti/Logs/DiscordMessages.db"
dbcon = sl.connect(str(dbpath))
#endregion



class LoggerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

#	@commands.Cog.listener("on_message")
#	async def logmessages(self, message):
#		await self.bot.process_commands(message)
#		if (message.guild.id == 764981968579461130) and (message.channel.id != 789195444957609994) and (message.channel.id != 789607866780745748):
#			sentmsg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+", "+str(message.channel.id)+", "+str(message.channel.name)+", "+str(message.author)+", "+str(message.content)
#			print(f"Message: {sentmsg}")
#			with open("logs/test.csv", 'a') as file_object:
#				file_object.write(sentmsg+"\n")

	@commands.Cog.listener("on_message")
	async def logmessages(self, message):
		sql = 'INSERT into Messages (created_at, msgid, guildid, channelid, authorid, guildname, channelname, authorname, message, url, attachments) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
		sqldata = [
				int(time.time()), 
				int(message.id),
				int(message.guild.id),
				int(message.channel.id),
				int(message.author.id),
				str(message.guild.name),
				str(message.channel.name),
				str(message.author),
				str(str(message.system_content)+str(message.embeds)),
				str(message.jump_url),
				str(message.attachments)
					]
		with dbcon:
			dbcon.execute(sql, sqldata)
	
	@commands.Cog.listener("on_message")
	async def logcommands(self, message):
		content = message.content
		if (content.startswith(prefix)):
			sql = 'INSERT into Commands (created_at, msgid, guildid, channelid, authorid, guildname, channelname, authorname, message, url) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
			sqldata = [
					int(time.time()), 
					int(message.id),
					int(message.guild.id),
					int(message.channel.id),
					int(message.author.id),
					str(message.guild.name),
					str(message.channel.name),
					str(message.author),
					str(message.content),
					str(message.jump_url)
					   ]
			with dbcon:
				dbcon.execute(sql, sqldata)

	
def setup(bot):
    bot.add_cog(LoggerCog(bot))

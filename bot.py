import discord
from discord.ext import commands
import json
import os

with open('setting.json','r',encoding='utf8') as jfile:
   jdata=json.load(jfile)

bot =commands.Bot(command_prefix='[')

for Filename in os.listdir('./cmds'):
   if Filename.endswith('.py'):
      bot.load_extension(F'cmds.{Filename[:-3]}')

@bot.event
async def on_ready():
   print("Bot is online 機器人已就位",discord.__version__)
   channel=bot.get_channel(int(jdata['chatchannel']))
   #await channel.send("Bot is online 機器人已就位")


@bot.command()
async def ping(ctx):
   await ctx.send(f'{round(bot.latency*1000)}(ms)')

@bot.command()
async def octuysup(ctx,extension):
   bot.reload_extension(f'cmds.{extension}')
   print('reload')

#@bot.event
#async def on_member_join(member):
#   print(f'{member}join!')

#@bot.event
#async def on_member_remove(member):
#   print(f'{member}gg!')

#@bot.command()
#async def test(ctx, arg):
#   await ctx.send(arg)
if __name__=="__main__":
   bot.run(jdata['TOKEN'])
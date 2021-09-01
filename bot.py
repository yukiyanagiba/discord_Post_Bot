import discord
from discord.ext import commands
import json
import os
import re
import logging, sys

with open('setting.json','r',encoding='utf8') as jfile:
   jdata=json.load(jfile)

logger= logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(jdata['IMG_DIR']+'kentaiBot2.log', 'w', 'utf-8')
formatter = logging.Formatter('[%(asctime)s] %(name)-12s: %(levelname)-8s %(message)s', '%Y/%m/%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
sys.stderr.write = logger.error
sys.stdout.write = logger.info

bot =commands.Bot(command_prefix='!')

for Filename in os.listdir('./cmds'):
   if Filename.endswith('.py'):
      bot.load_extension(F'cmds.{Filename[:-3]}')

@bot.event
async def on_ready():
   print("Bot is online 機器人已就位",discord.__version__)
   print("Name: {}".format(bot.user.name))
   print("ID: {}".format(bot.user.id))
   channel=bot.get_channel(int(jdata['chatchannel']))
   #await channel.send("Bot is online 機器人已就位")

#msg.content
@bot.command()
async def ping(ctx):
   await ctx.send(f'{round(bot.latency*1000)}(ms)')

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
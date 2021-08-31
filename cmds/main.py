import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,re


class Main(Cog_Extension):

   with open('setting.json','r',encoding='utf8') as jfile:
      jdata=json.load(jfile)

   @commands.command()
   async def ssghtfvh(self,ctx, arg):
      await ctx.send(arg)

   @commands.command()
   async def reloadModule(self,ctx,extension):#重新載入某個extension
      self.bot.reload_extension(f'cmds.{extension}')
      print('reload module')

   @commands.command()
   async def addRule(self,ctx,msg):#新增表情加入身分組規則
      p1=re.compile('_')
      a=p1.search(msg)
      q1=int(msg[:a.start()])
      msg=msg[a.start()+1:]
      p2=re.compile('=')
      a=p2.search(msg)
      q2=msg[:a.start()]
      q3=msg[a.start()+1:]
      print(ctx.author,"加入規則 文章編碼:",q1," 表情:",q2," 身分組:",q3)
      self.jdata['emoji_role'].append({"message_id": q1,"emojiname": q2,"roleassign": q3})
      with open('setting.json', 'w',encoding='utf8') as jsonfile:
         json.dump(self.jdata, jsonfile, indent=4)
      self.bot.get_cog('Event').roleAssign=True

   @commands.command()
   async def addBadGuy(self,ctx,msg):#新增黑名單
      self.jdata['badGuy'].append({"member_id": int(msg)})
      with open('setting.json', 'w',encoding='utf8') as jsonfile:
         json.dump(self.jdata, jsonfile, indent=4)
      self.bot.get_cog('Event').badGuyAssign=True
      print(ctx.author,"將",msg,"加入黑名單")

   @commands.command()
   async def delRule(self,ctx,msg):#刪規則
      for i in range(len(self.jdata['emoji_role'])):
         if msg==self.jdata['emoji_role'][i]["roleassign"]:
            self.jdata['emoji_role'].pop(i)
            break
      with open('setting.json', 'w',encoding='utf8') as jsonfile:
         json.dump(self.jdata, jsonfile, indent=4)
      self.bot.get_cog('Event').roleAssign=True
      print(ctx.author,"刪除規則",msg)

   @commands.command()
   async def delBadGuy(self,ctx,msg):#刪黑名單
      for i in range(len(self.jdata['badGuy'])):
         if int(msg)==self.jdata['badGuy'][i]["member_id"]:
            self.jdata['badGuy'].pop(i)
            break
      with open('setting.json', 'w',encoding='utf8') as jsonfile:
         json.dump(self.jdata, jsonfile, indent=4)
      self.bot.get_cog('Event').badGuyAssign=True
      print(ctx.author,"刪除黑名單",msg)

   @commands.command()
   async def printBotStatus(self,ctx):#列出目前狀態
      for i in range(len(self.jdata['emoji_role'])):
         await ctx.send(self.jdata['emoji_role'][i])
      for i in range(len(self.jdata['badGuy'])):
         await ctx.send(self.jdata['badGuy'][i])

def setup(bot):
   bot.add_cog(Main(bot))
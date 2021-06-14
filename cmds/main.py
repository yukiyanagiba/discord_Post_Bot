import discord
from discord.ext import commands
from core.classes import Cog_Extension


class Main(Cog_Extension):
   @commands.command()
   async def ssghtfvh(self,ctx, arg):
      await ctx.send(arg)

def setup(bot):
   bot.add_cog(Main(bot))
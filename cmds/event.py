import os
import datetime
import discord
import json,random
import requests
import re
import tweepy
import random
import codecs
import urllib.request
import ehapi
from discord.ext import commands
from core.classes import Cog_Extension
from plurk_oauth import PlurkAPI
from pathlib import Path
from bs4 import BeautifulSoup

BASE = "https://cdn.discordapp.com/attachments/306823976615936002/"
G_CATEGORY = {
    "Doujinshi": BASE + "471642768180117524/doujinshi.png",
    "Manga": BASE + "471642771862716446/manga.png",
    "Artist CG": BASE + "471642764623478804/artistcg.png",
    "Game CG": BASE + "471642769169842176/gamecg.png",
    "Western": BASE + "471642775964745729/western.png",
    "Non-H": BASE + "471642774350069771/non-h.png",
    "Image Set": BASE + "471642770331926558/imageset.png",
    "Cosplay": BASE + "471642766993260544/cosplay.png",
    "Asian Porn": BASE + "471642765781106689/asianporn.png",
    "Misc": BASE + "471642773087322112/misc.png"
}
EH_COLOUR = discord.Colour(0x660611)

class Event(Cog_Extension):
   #以下pixiv
   p1=re.compile('www\.pixiv\.net\/member_illust\.php')
   p2=re.compile('www\.pixiv\.net\/artworks')
   p3=re.compile('www\.pixiv\.net\/en\/artworks')
   #以下twitter
   p4=re.compile('twitter\.com\/(\w{0,60})\/status')
   p5=re.compile('t\.co\/')
   #以下plurk
   p6=re.compile('www\.plurk\.com\/p')
   #以下eh
   p7=re.compile('e-hentai\.org\/g\/')
   p8=re.compile('exhentai\.org\/g\/')
   #以下yande
   p9=re.compile('yande\.re\/post\/show\/')
   p10=re.compile('https:\/\/files\.yande\.re\/sample\/.*\.jpg","sample_width')
   with open('setting.json','r',encoding='utf8') as jfile:
      jdata=json.load(jfile)
   
   # Random User Agent List
   USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
   ]

   USER_AGENT = random.choice(USER_AGENT_LIST)
   headers = {
     'user-agent': USER_AGENT
   }

   list_message_id=[]
   list_emojiname=[]
   list_roleassign=[]
   list_badGuy=[]
   roleAssign=True
   badGuyAssign=True

   @commands.Cog.listener()
   async def on_raw_reaction_add(self,payload):
      if not self.badGuyAssign:
         pass
      else:
         with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
         self.list_badGuy=[]
         for i in range(len(jdata['badGuy'])):
            self.list_badGuy.append(jdata['badGuy'][i]['member_id'])
         self.badGuyAssign=False

      if not self.roleAssign:
         pass
      else:
         with open('setting.json','r',encoding='utf8') as jfile:
            jdata=json.load(jfile)
         self.list_message_id=[]
         self.list_emojiname=[]
         self.list_roleassign=[]
         for i in range(len(jdata['emoji_role'])):
            self.list_message_id.append(jdata['emoji_role'][i]['message_id'])
            self.list_emojiname.append(jdata['emoji_role'][i]['emojiname'])
            self.list_roleassign.append(jdata['emoji_role'][i]['roleassign'])
         self.roleAssign=False

      for i in range(len(self.list_message_id)):
         if payload.message_id==self.list_message_id[i] and payload.emoji.name==self.list_emojiname[i]:
            role = discord.utils.get(payload.member.guild.roles, name=self.list_roleassign[i])
            if payload.member.id not in self.list_badGuy:
               await payload.member.add_roles(role)
               print(payload.member,self.list_roleassign[i])
            else:
               print(payload.member,"在黑名單")
               break

      channel = await self.bot.fetch_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      url=""
      if message.author.id==self.bot.user.id and payload.emoji.name=="idk":
         print(message.embeds)
         if message.embeds!=[]:
            url=message.embeds[0].image.url
            p1=re.compile('\#')
            a=p1.search(url)
            if a==None:
               url+="#1"
            else:
               num=int(url[a.start()+1:])+1
               url=url[:a.start()]+"#"+str(num)
            embed=message.embeds[0]
            embed.set_image(url=url)
            await message.edit(embed=embed)
         else:
            url=message.content
            p1=re.compile('\#')
            a=p1.search(url)
            if a==None:
               url+="#1"
            else:
               num=int(url[a.start()+1:])+1
               url=url[:a.start()]+"#"+str(num)
            await message.edit(content=url)

   @commands.Cog.listener()
   async def on_message(self,msg):
      k=False
      chr={}
      strf=''
      askNum=1
      twitterMedia=None
      
      isExplicit=False
      # check message is explicit ?
      if msg.content.count("||") == 2:
        isExplicit=True
        msg.content.replace("||","")
        
      print(msg.author,msg.content)
      #以下pixiv
      a=self.p1.search(msg.content)
      if a==None:
         a=self.p2.search(msg.content)
         if a==None:
            a=self.p3.search(msg.content)
      if a!=None:
         k=True
         strf = re.search('\d{3,9}', msg.content[a.start():]).group()

      for i in range(len(msg.embeds)):
         chr=msg.embeds[i].to_dict()

      if k and msg.author!=self.bot.user:
         colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
         uId,uName,illustTitle,illustComment,pageCount,image_url=self.pixivMetadata(strf)
         if "ugoira" in image_url:
            image_url=self.pixivDLGIF2URL(image_url)
            # pre-cache for server
            requests.get(image_url,headers = self.headers)
            requests.get(image_url,headers = self.headers)
            if isExplicit:
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
                embed.set_image(url=image_url)
                embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
                await msg.channel.send(embed=embed)
         elif pageCount>1:
            askpage = re.search('P\d{1,2}', msg.content[a.start():].upper())
            allpage = re.search('ALL', msg.content[a.start():].upper())
            if askpage:
               if int(askpage.group()[1:])>0 and int(askpage.group()[1:])<pageCount+1:
                  askNum=int(askpage.group()[1:])
                  pageNum="_p"+str(askNum-1)
                  image_url=self.pixivDL2URL(image_url.replace('_p0',pageNum))
                  if isExplicit:
                      await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
                  else:
                      embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
                      embed.set_image(url=image_url)
                      embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
                      await msg.channel.send(embed=embed)
            elif allpage:
               for page in range(1,pageCount+1):
                    pageNum="_p"+str(page-1)
                    image_url=self.pixivDL2URL(image_url.replace('_p0',pageNum))
                    await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                  image_url=self.pixivDL2URL(image_url)
                  if isExplicit:
                      await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
                  else:
                      embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
                      embed.set_image(url=image_url)
                      embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
                      await msg.channel.send(embed=embed)
         else:
            image_url=self.pixivDL2URL(image_url)
            if isExplicit:
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
                embed.set_image(url=image_url)
                embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
                await msg.channel.send(embed=embed)
         try:
            if not isExplicit:
                await msg.edit(suppress=True)
         except:
            print('沒有關閉embed的權限')
      #以下twitter
      a=self.p4.search(msg.content)
      if a!=None:
         #twitter oauth
         auth = tweepy.OAuthHandler(self.jdata['consumer_key'], self.jdata['consumer_secret'])
         auth.set_access_token(self.jdata['access_token'], self.jdata['access_token_secret'])
         api = tweepy.API(auth)
      
         strf = re.search('\d{15,20}', msg.content[a.start():]).group()
         status = api.get_status(strf, tweet_mode="extended")
         try:
            twitterMedia=status.extended_entities['media']
            k=True
         except AttributeError:  #twitter沒圖片
            pass
         if k and msg.author!=self.bot.user:
            if len(status.extended_entities['media'])==1:
               try:
                  twitterMedia=status.extended_entities['media'][0]['video_info']
                  bitrate = 0
                  maxIndex = 0
                  for index in range(len(twitterMedia['variants'])):
                    if twitterMedia['variants'][index]['content_type'] == "video/mp4" and twitterMedia['variants'][index]['bitrate'] > bitrate:
                        bitrate = twitterMedia['variants'][index]['bitrate']
                        maxIndex = index
                  await msg.channel.send(self.msgSendProcess(twitterMedia['variants'][maxIndex]['url'], isExplicit))
               except KeyError:  #twitter沒影片
                  pass
                  
            else:
               colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
               uId=status.user.screen_name
               uName=status.user.name
               illustTitle=status.full_text
               a=self.p5.search(illustTitle)
               illustTitle=illustTitle[:a.start()-9]
               image_url=twitterMedia[0]['media_url_https']
               if isExplicit:
                   await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
               else:
                   embed=discord.Embed(title=illustTitle,url="https://twitter.com/"+uId+"/status/"+strf, color=colonn)
                   embed.set_image(url=image_url)
                   embed.set_author(name=uName, url="https://twitter.com/"+uId)
                   await msg.channel.send(embed=embed)
               for i in range(1,len(status.extended_entities['media'])):
                  await msg.channel.send(self.msgSendProcess(twitterMedia[i]['media_url_https'], isExplicit))
               try:
                  if not isExplicit:
                    await msg.edit(suppress=True)
               except:
                  print('沒有關閉embed的權限')
      #以下plurk
      a=self.p6.search(msg.content)
      if a!=None:
         #plurk oauth
         plurk = PlurkAPI(self.jdata['plurk_consumer_key'], self.jdata['plurk_consumer_secret'])
         plurk.authorize(self.jdata['plurk_access_token'], self.jdata['plurk_access_token_secret'])
           
         url = re.search("(?P<url>https?://www.plurk.com/p/[^\s]{6})", msg.content).group("url")
         plurk_id = int((url.rsplit('/', 1)[-1]), 36)
         json_object_string = plurk.callAPI('/APP/Timeline/getPlurk', options={'plurk_id': plurk_id})
         owner_id = json_object_string['plurk']['owner_id']
         nick_name = json_object_string['plurk_users'][str(owner_id)]['nick_name']
         if json_object_string:
             content_string = json_object_string['plurk']['content']
             try:
                 image_url = re.search("(?P<url>https?://images.plurk.com/[^\s]+.(?:png|jpg|gif))", content_string).group("url")
                 colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
                 if isExplicit:
                     await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
                 else:
                     embed=discord.Embed(title='plurk',url=url, color=colonn)
                     embed.set_image(url=image_url)
                     embed.set_author(name=nick_name, url="https://www.plurk.com/"+nick_name)
                     await msg.channel.send(embed=embed)
                 allpage = re.search('ALL', msg.content[a.start():].upper())
                 if allpage:
                    image_urls = re.findall("(?P<url>https?://images.plurk.com/(?!mx_)[^\s]+.(?:png|jpg|gif))", content_string, re.DOTALL)
                    image_urls_dedupe = []
                    for index in range(len(image_urls)):
                        if image_urls[index] not in image_urls_dedupe:
                            image_urls_dedupe.append(image_urls[index])
                    list_len = len(image_urls_dedupe)
                    if list_len > 1:
                        for index in range(1, list_len):
                            await msg.channel.send(self.msgSendProcess(image_urls_dedupe[index], isExplicit))
             except AttributeError:  #plurk沒圖片
                 print("image url not found")
         else:
             print("plurk not found")
      #以下eh
      a=self.p7.search(msg.content)
      ispage = 0
      if a==None:
         a=self.p8.search(msg.content)
         if a==None:
            a=ehapi.page_token.search(msg.content)
            if a!=None:
                ispage = 1
      if a!=None:
            if isExplicit:
                urlstring = re.search("(?P<url>https?://e(-|x)hentai.org/g/[\d]+/[a-z0-9]+)", msg.content).group("url")
                if urlstring[-1] == "/":
                    gallery_id = urlstring.split("/")[-3]
                    gallery_token = urlstring.split("/")[-2]
                else:
                    gallery_id = urlstring.split("/")[-2]
                    gallery_token = urlstring.split("/")[-1]
                token_group = [[gallery_id,gallery_token]]
                gmetadata = ehapi.api_gallery(token_group)
                msg_ret = ""
                rating = int(float(gmetadata[0]['rating']))
                for i in range(rating):
                    msg_ret += "★"
                try:
                    title = gmetadata[0]['title_jpn']
                except:
                    title = gmetadata[0]['title']
                msg_ret = msg_ret + "\n" + title
                await msg.channel.send(msg_ret)
                image_url = gmetadata[0]['thumb']
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                galleries = ehapi.get_galleries(msg.content)
                if galleries:
                    if len(galleries) > 5:  # don't spam chat too much if user spams links
                        await msg.channel.send(embed=embed_titles(galleries))
                    else:
                        for gallery in galleries:
                            await msg.channel.send(embed=embed_full(gallery))
            try:
                if not isExplicit:
                    await msg.edit(suppress=True)
            except:
               print('沒有關閉embed的權限')
               
      #以下yande
      a=self.p9.search(msg.content)
      if a!=None:
        url = re.search('(?P<url>https?:\/\/yande\.re\/post\/show\/(\d+))', msg.content).group("url")
        r =  requests.get(url,headers = self.headers)
        if r.text.find("Rating: Explicit") != -1:
            image_url = self.p10.search(r.text).group(0)[:-15]
            colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
            if isExplicit:
                await msg.channel.send(self.msgSendProcess(image_url, isExplicit))
            else:
                embed=discord.Embed(title='yande.re',url=image_url, color=colonn)
                embed.set_image(url=image_url)
                await msg.channel.send(embed=embed)
            try:
                await msg.edit(suppress=True)
            except:
                print('沒有關閉embed的權限')

   # post process msg content
   def msgSendProcess(self,str,flag):
        if not flag:
            return str
        else:
            return "|| " + str + " ||"

   # get pixiv data
   def pixivMetadata(self,id):
        r =  requests.get("https://www.pixiv.net/artworks/"+id,headers = self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        meta=soup.find_all('meta')
        content=meta[25].get('content')
        content=content.replace('false','\"false\"').replace('true','\"true\"').replace('null','\"null\"')

        jdata=json.loads(content)
        
        return jdata['illust'][id]['userId'],jdata['illust'][id]['userName'],jdata['illust'][id]['illustTitle'],jdata['illust'][id]['illustComment'],jdata['illust'][id]['userIllusts'][id]['pageCount'],jdata['illust'][id]['urls']['original']
        
   # download pixiv image and return image url on server
   def pixivDL2URL(self,img_url):
        IMG_DIR = self.jdata['IMG_DIR']
        DOMAIN = self.jdata['DOMAIN']
    
        # Get image id and extension
        img_id = img_url.rsplit('/', 1)[-1].split('_', 1)[0]
        img_page = img_url.rsplit('/', 1)[-1].split('_', 1)[1].split('.',1)[0].split('_',1)[0]
        img_path = os.path.join(IMG_DIR, img_id + "_" + img_page +".jpg")
        
        if not os.path.isfile(img_path):
            # Create opener with pixiv referer
            opener = urllib.request.build_opener()
            opener.addheaders = [('user-agent', self.USER_AGENT)]
            opener.addheaders = [('referer','https://www.pixiv.net/')]
            
            urllib.request.install_opener(opener)
            # Download image
            urllib.request.urlretrieve(img_url, img_path)
            
            # Compress image with pngquant
            command = "convert " + img_path + " " + img_path
            os.system(command)
        
        domain_url = DOMAIN + img_id + "_" + img_page +".jpg"
        print(domain_url)
        return domain_url
        
   # download pixiv animate image by pixivutil and return image url on server
   def pixivDLGIF2URL(self,img_url):
        IMG_DIR = self.jdata['IMG_DIR']
        DOMAIN = self.jdata['DOMAIN']
    
        # Get image id
        img_id = img_url.rsplit('/', 1)[-1].split('_', 1)[0]
        img_path = os.path.join(IMG_DIR, img_id + ".gif")
        imgzip_path = os.path.join(IMG_DIR, img_id + ".zip")
        
        if not os.path.isfile(img_path):
            # Create opener with pixiv referer
            opener = urllib.request.build_opener()
            opener.addheaders = [('user-agent', self.USER_AGENT)]
            opener.addheaders = [('referer','https://www.pixiv.net/')]
            
            urllib.request.install_opener(opener)
            # Download image
            imgzip_url = img_url.replace("/img-original/", "/img-zip-ugoira/").replace('_ugoira0.jpg','_ugoira600x600.zip')
            urllib.request.urlretrieve(imgzip_url, imgzip_path)
            
            # Convert zip to gif with ffmpeg
            command = "cd "+IMG_DIR+" && 7z x -o"+img_id+" "+img_id+".zip && rm "+img_id+".zip && gifgen -o "+img_id+".gif "+img_id+"/%06d.jpg && rm -rf "+img_id
            os.system(command)
        
        domain_url = DOMAIN + img_id + ".gif"
        print(domain_url)
        return domain_url
    
# string of titles for lots of links
def embed_titles(exmetas):
    link_list = [create_markdown_url(exmeta['title'], create_ex_url(exmeta['gid'], exmeta['token'])) for exmeta in
                 exmetas]
    msg = "\n".join(link_list)
    return discord.Embed(description=msg,
                         colour=EH_COLOUR)


# pretty discord embeds for small amount of links
def embed_full(exmeta):
    em = discord.Embed(title=BeautifulSoup(exmeta['title'], "html.parser").string,
                       url=create_ex_url(exmeta['gid'], exmeta['token']),
                       timestamp=datetime.datetime.utcfromtimestamp(int(exmeta['posted'])),
                       description=BeautifulSoup(exmeta['title_jpn'], "html.parser").string,
                       colour=EH_COLOUR)
    em.set_image(url=exmeta['thumb'])
    em.set_thumbnail(url=G_CATEGORY[exmeta['category']])
    em.set_footer(text=exmeta['filecount'] + " pages")
    em.add_field(name="rating", value=exmeta['rating'])
    em = process_tags(em, exmeta['tags'])
    return em


# put our tags from the EH JSON response into the discord embed
def process_tags(em, tags):
    tag_dict = {'male': [], 'female': [], 'parody': [], 'character': [], 'misc': []}
    for tag in tags:
        if ":" in tag:
            splitted = tag.split(":")
            if splitted[0] in tag_dict:
                tag_dict[splitted[0]].append(BeautifulSoup(splitted[1], "html.parser").string)
        else:
            tag_dict['misc'].append(tag)

    def add_field(ex_tag):
        if tag_dict[ex_tag]:
            em.add_field(name=ex_tag, value=', '.join(tag_dict[ex_tag]))

    add_field("male")
    add_field("female")
    add_field("parody")
    add_field("character")
    add_field("misc")
    return em


# make a markdown hyperlink
def create_markdown_url(message, url):
    return "[" + BeautifulSoup(message, "html.parser").string + "](" + url + ")"


# make a EH url from it's gid and token
def create_ex_url(gid, g_token):
    return "https://exhentai.org/g/" + str(gid) + "/" + g_token + "/"    

def setup(bot):
   bot.add_cog(Event(bot))
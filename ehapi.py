import json
import re
import discord
import requests
import datetime
import json
from bs4 import BeautifulSoup

page_token = re.compile('https?:\/\/e[\-x]hentai\.org\/s\/([\da-f]{10})\/(\d+)\-(\d+)')
gallery_token = re.compile('https?:\/\/e[\-x]hentai\.org\/(?:g|mpv)\/(\d+)\/([\da-f]{10})')
EH_API = "https://api.e-hentai.org/api.php"
EH_COLOUR = discord.Colour(0x660611)
ICON_EH_BASE = "https://cdn.discordapp.com/attachments/306823976615936002/"

G_CATEGORY = {
    "Doujinshi": ICON_EH_BASE + "471642768180117524/doujinshi.png",
    "Manga": ICON_EH_BASE + "471642771862716446/manga.png",
    "Artist CG": ICON_EH_BASE + "471642764623478804/artistcg.png",
    "Game CG": ICON_EH_BASE + "471642769169842176/gamecg.png",
    "Western": ICON_EH_BASE + "471642775964745729/western.png",
    "Non-H": ICON_EH_BASE + "471642774350069771/non-h.png",
    "Image Set": ICON_EH_BASE + "471642770331926558/imageset.png",
    "Cosplay": ICON_EH_BASE + "471642766993260544/cosplay.png",
    "Asian Porn": ICON_EH_BASE + "471642765781106689/asianporn.png",
    "Misc": ICON_EH_BASE + "471642773087322112/misc.png"
}


# extract all exurls from a string and get the metadata
def get_galleries(message):
    gids = get_gids(message)
    all_galleries = []
    if gids:
        for token_group in divide_chunks(gids):
            all_galleries += api_gallery(token_group)
    return all_galleries


# get the gids and hashes of every EH url posted in a message
def get_gids(message):
    gallery_results = []
    page_results = page_token.findall(message)
    # fix up ordering and types before querying EH
    remapped_results = [[int(elem[1]), elem[0], int(elem[2])] for elem in page_results]
    # divide into chunks of max 25 requests per POST to EH
    for token_group in divide_chunks(remapped_results):
        gallery_results += api_page(token_group)
    gallery_results += [[int(elem[0]), elem[1]] for elem in gallery_token.findall(message)]
    return gallery_results


# Divide lists into chunks of 25 since EH only allows a max of 25 urls per POST request
def divide_chunks(original_chunk):
    return [original_chunk[i:i + 25] for i in range(0, len(original_chunk), 25)]


# Query the EH api for gid from a gallery page url
def api_page(token_group):
    payload = {"method": "gtoken", "pagelist": token_group}
    r = requests.post(EH_API, data=json.dumps(payload))
    return [[elem['gid'], elem['token']] for elem in r.json()['tokenlist']]


# Query the EH api for metadata from a gallery
def api_gallery(token_group):
    payload = {"method": "gdata", "gidlist": token_group, "namespace": 1}
    r = requests.post(EH_API, data=json.dumps(payload))
    return r.json()['gmetadata']

    
# string of titles for lots of links
def embed_titles(exmetas):
    link_list = [create_markdown_url(exmeta['title'], create_ex_url(exmeta['gid'], exmeta['token'])) for exmeta in
                 exmetas]
    msg = "\n".join(link_list)
    return discord.Embed(description=msg,
                         colour=EH_COLOUR)


# pretty discord embeds for small amount of links
def embed_full(exmeta,isExplicit):
    em = discord.Embed(title=BeautifulSoup(exmeta['title'], "html.parser").string,
                       url=create_ex_url(exmeta['gid'], exmeta['token']),
                       timestamp=datetime.datetime.utcfromtimestamp(int(exmeta['posted'])),
                       description=BeautifulSoup(exmeta['title_jpn'], "html.parser").string,
                       colour=EH_COLOUR)
    if not isExplicit:
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
    

import os
import discord
import discord_interactive
import urllib.request
import urllib
import re
import youtube_dl
import nacl
import asyncio
import json
import tracemalloc
import urlparse2
import pyshorteners

from discord.ext import commands


global is_playingSong
global is_Looping
is_Looping = False
video_ids = ""
info_dict = ""
video_title=""
queue = []
is_playingSong = False
video_duration_int = 0
title=""

async def process_play(ctx, url,client,is_Online):
  #Formato que utilizamos para el video que descargamos
  global video_ids
  global info_dict
  global voice
  global video_duration_int
  global video_duration_str
  global video_title
  global is_playingSong
  global id
  global queue
  print(is_playingSong)
  song_there = os.path.isfile("song.mp3")
  try:
    if not is_playingSong:
      if song_there:
        os.remove("song.mp3")
  except PermissionError:
      await ctx.send("HEY PENDEJO YA HAY UNA")
      return
  if is_Online:
    if not is_playingSong:
      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
      try:
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
      except:
        await ctx.send("Alch no encontre tu mamada")
        return
      
      ydl_opts = {
      "format": "bestaudio/best",
      "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
        }],
      }
       #Con youtube_dl descarga la url y una vez
       #termino la descarga, la reproduce
       
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info("https://www.youtube.com/watch?v=" + video_ids[0], download=False)
      video_title = info_dict.get("title")
      video_duration_str = str(info_dict.get('duration', None))
      video_duration_int = int(info_dict.get('duration', None))
      ydl.download(["https://www.youtube.com/watch?v=" + video_ids[0]])
      queue.append("https://www.youtube.com/watch?v=" + video_ids[0])
      for file in os.listdir("./"):
        if file.endswith(".mp3"):
          os.rename(file, "song.mp3")
    else:
      queue_title = await mini_Src(url)
      print ("Ajajaja que pedo como llegue aqui")
      await ctx.send("Cancion listada "+ queue_title)
      queue.append(await src_Data(queue_title,url))
        
        
async def prt_Queue(ctx):
  global queue
  a = 0
  print(len(queue))
  while not a == len(queue):
    await ctx.send(str(a+1)+".- "+queue[a])
    a = a+1
    
  


async def mini_Src(urlM):
  global ydl_opts
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urlM)
  try:
   video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
  except:
    return
  ydl_opts_src = {
    "format": "bestaudio/best",
    "postprocessors": [{
     "key": "FFmpegExtractAudio",
      "preferredcodec": "mp3",
      "preferredquality": "192",
      }],
    }
  with youtube_dl.YoutubeDL(ydl_opts_src) as ydl:
    info_dict = ydl.extract_info("https://www.youtube.com/watch?v=" + video_ids[0], download=False)
  vtitle = info_dict.get("title")
  return(vtitle)

async def src_Data(arg,keyword):
  global id
  k=0
  print(arg)
  urlv = ""
  title = ""
  url = keyword.replace(" ", "+")
  #Parte que busca la lista de videos
  html_search = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
  video_ids_search = re.findall(r"watch\?v=(\S{11})", html_search.read().decode())
  while not arg == title:
    id = video_ids_search[k]
    urlv = "https://www.youtube.com/watch?v="+id
    params = {"format": "json", "url": urlv}
    link = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    link = link + "?" + query_string
    k = k + 1
    with urllib.request.urlopen(link) as response:
      response_text = response.read()
      data = json.loads(response_text.decode())
    print(title)
    title = (data['title'])
  return (urlv)

async def src_Down(link):
  global info_dict
  global video_duration_int
  global video_duration_str
  global video_title
  global is_playingSong
  song_there = os.path.isfile("song.mp3")
  try:
    if not is_playingSong:
      if song_there:
        os.remove("song.mp3")
  except PermissionError:
    return
  ydl_opts = {
  "format": "bestaudio/best",
  "postprocessors": [{
    "key": "FFmpegExtractAudio",
    "preferredcodec": "mp3",
    "preferredquality": "192",
    }],
  }
   #Con youtube_dl descarga la url y una vez
    #termino la descarga, la reproduce

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(link , download=False)
  video_title = info_dict.get("title")
  video_duration_str = str(info_dict.get('duration', None))
  video_duration_int = int(info_dict.get('duration', None))
  ydl.download([link])
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
       os.rename(file, "song.mp3")


async def played(ct,clien):
  ctx = ct
  client = clien
  global voice
  global video_duration_int
  global video_duration_str
  global video_title
  global video_download
  global short_url
  global video_url
  global is_playingSong
  global queue
  global is_Looping
  if not is_playingSong:
    print("Ya llegue")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    is_playingSong = True
    print(is_playingSong)
    print("Deberia empezar la cancion")
    if is_Looping == False:
      await ctx.send("Se esta reproduciendo " + video_title)
    await asyncio.sleep(video_duration_int+1)
    if is_Looping == False:
      await ctx.send("Ya acabo la puta cancion pon otra no seas webon, esta madre duro "+ video_duration_str + " segundos watefok tu papa barriendo ")
      is_playingSong = False
      try:
        queue.pop(0)
        await src_Down(queue[0])
        await played(ctx,client)
      except:
        print("Muerete alv")
    else:
      print("Ya llegue")
      is_playingSong = False
      await played(ctx,client)



async def get_Data():
  global video_ids
  global info_dict
  global id
  global queue
  video_title = info_dict.get("title",None)
  video_url = queue[0]
  return("Estas escuchando: \n" +video_title +"\n "+video_url)

async def get_Song():
  global video_download
  global short_url
  global info_dict
  video_download = info_dict.get("url",None)
  try:
    shortener = pyshorteners.Shortener()
    short_url = shortener.dagd.short(video_download)
    return(short_url)
  except:
    return(video_download)

async def set_Loop():
  global is_Looping
  if is_Looping == False:
    is_Looping = True
    return(queue[0] + " esta en loop")
  else:
    is_Looping = False
    return("Esta madre ya no esta en loop")
  


#Bot god(biblias epicas)
#WENAAAAAS BUENAAAAAAAAAAAAS Chango caca
#Ya entendi que le moviste OJITO
#El conenct jala cuando utilizas cualquier comando? o es el -connect? Eso es mas que suficiente XD COn el que no pete el BURGIR xdddxddd
#Es un comando a parte pero no explota por el numero que tenemos de validacion
#Oye sabes como hacer un virtual enviroment???? AL paracer se necesita para que funcione lo del sql y asi conectarlo a mi base de datos y le metemos cuanta mamada queramos
#WUAT. No te lo manejo, pero puedo buscarlo en otro rato
#Ahorita es lo que estoy buscando pero no le se xd
#https://www.geeksforgeeks.org/python-virtual-environment/
#Medio de vistazo se ve bien
#Wtf dice que segun se instala desde el shell pip install virtualenv
#Smn XD. Esa pagina me gusta bastantio asi que medio le tengo confianza
#Ya lo estoy instalando a ya se instalo xd (EZ) xd
#Regreso en un momentio, ando en clase <----- Un puto god not not not not gay al cuadrado Le saca la raiz cuadrada NUUUUU *c viene en el bot* mmmmmmmmmm xd Ya vayase a su clase aca lo espero vaa
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
import rutinas
import urlparse2

from rutinas import *
from asyncio import *
from discord.ext import commands

my_burgir = os.environ['burgir']

#Prefijo para los comandos
client = commands.Bot(command_prefix="-")

is_Online = False
is_Queue = False
ydl_opts = ""
video_ids = ""
is_Selecting = True
songs=[]
queue = []
players = []
video_duration_int = 0
video_duration_str = ""
i = 0
link = ""


@client.command()
async def connect(ctx):
  global is_Online
  if is_Online:
    await ctx.send("Ya estoy adentro tonto")
  else:
    is_Online = True
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = str(ctx.author.voice.channel))
    await voiceChannel.connect()



#Funcion pa que se conecte el bot pndjo
@client.command(aliases = ['p','cantale','cantaleperra','esclavo','reneputo'])
async def play(ctx, *, arg):
  global queue
  global ydl_opts
  global video_ids
#  print(arg)
  url = arg.replace(" ", "_")
#  print(url)
# Para ya no poner url
# Checa si ya hay una cancion en reproduccion

#Creamos la variable en la que el bot vive y lo conectamos a un canal
  global is_Online
  if not is_Online:
    is_Online = True
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    await voiceChannel.connect()
  await rutinas.process_play(ctx,url,client,is_Online)
  
  await rutinas.played(ctx,client)
#Formato que utilizamos para el video que descargamos

@client.command(aliases = ["s","buscar","b"])
async def search(ctx, *, arg):
  global is_Online
  if not is_Online:
    is_Online = True
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))
    await voiceChannel.connect()
  await ctx.send("Aver andale cabron escoge tu mamada")
  
  url = arg.replace(" ", "_")
  #Parte que busca la lista de videos
  html_search = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
  video_ids_search = re.findall(r"watch\?v=(\S{11})", html_search.read().decode())
  #Variables chafas
  global i
  songs=[]
  lista = ""
  f = 0
  #Ciclo para hacer la lista
  while f <= 6:
    try:
      id = str(video_ids_search[f])
    except IndexError:
      await ctx.send("Me dio hueva buscar cosas tonto")
      return
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % id}
    link = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    link = link + "?" + query_string

    with urllib.request.urlopen(link) as response:
      response_text = response.read()
      data = json.loads(response_text.decode())
    songs.append(data['title'])
    lista = lista + (str(f)+".- "+songs[f]+"\n")
    f = f +1
  lista = lista + "cancel.- Para cancelar la seleccion"
  await ctx.send(lista)

  #Evento para detectar que cancion quieres
  
  @client.event
  async def on_message(message):
    if message.author.id == client.user.id:
      return
    global is_Selecting
    is_Selecting = True
    numeros = ['0', '1','2','3','4','5','6']
    if any(i in message.content for i in numeros) and is_Selecting:
      is_Selecting = False
      num = int(message.content)
      if not rutinas.is_playingSong:
        try:
          await rutinas.src_Down(await rutinas.src_Data(songs[num],url))
        except:
          await ctx.send("La neta no te entendi carnal puedes buscar otra vez u otra mamada que no tan mamadora?")
        print(str(rutinas.is_playingSong)+"WATEFOK")
        rutinas.queue.append(await rutinas.src_Data(songs[num],songs[num]))
        await rutinas.played(ctx,client)
      else:
        print("Jaja que pedo si sirve")
        titsrc = await rutinas.src_Data(songs[num],songs[num])
        await ctx.send("Cancion listada: "+ songs[num])
        rutinas.queue.append(titsrc)      
    if "cancel" in message.content:
      is_Selecting = False
      await ctx.send("Tons pa que me hablas tonto?")
    await client.process_commands(message)


@client.command()
async def queue(ctx):
  try:
   await rutinas.prt_Queue(ctx)
  except:
    await ctx.send("VETE A LA VRG")


@client.command()
async def loop(ctx):
  try:
    await ctx.send(await rutinas.set_Loop())
  except:
    await ctx.send("No hay nada reproduciendose estas tonto")  

@client.command()
async def current(ctx):
  try:
    await ctx.send(await rutinas.get_Data())
  except:
    await ctx.send("No hay nada que mostrar tonto")



@client.command()
async def stop(ctx):
  if is_Online:
    rutinas.is_playingSong = False
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def download(ctx):
  await ctx.send("Descarga la cancion: \n"+await rutinas.get_Song())



#Funcion para que resuma la hamburguesa
@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
      voice.resume()
  else:
      await ctx.send("YA LO PASADO PASAAAADO (Ya ta resumido)")



#Funcion para que se vaya(del McDonalds)
@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  global is_Online
  if is_Online:
    rutinas.is_playingSong = False
    is_Online = False
    await ctx.send("Nos vemos joputas")
    await voice.disconnect()
  else:
    await ctx.send("Deje dormir vrg pongase a jalar.")



#Funcion para que deje de burgir
@client.command()
async def pause (ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("Ya esta pausado wey no seas castroso")

print("Inicio el bot")


#Pa que corra chido
client.run(my_burgir)
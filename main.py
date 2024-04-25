import requests
from bs4 import BeautifulSoup
import discord 
from discord import Intents
from discord.ext import commands
import os
import boto3
import user
import video
from dotenv import load_dotenv
from datetime import datetime
import math
import clean
import uuid
import asyncio
import logging


logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 


boto3.setup_default_session(profile_name="brianliu")
table_name = "clip-manager"





# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("TOKEN")
CLOUDFRONT_URL = os.getenv("cloudfront_url")
table_name = "clip-manager"


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)



@bot.command()
async def clips(ctx, *args):
    user_queried = ctx.author
    if len(args) > 2:
        await ctx.send("Invalid Number of Arguments")
        return
    elif len(args) == 2:
        async for guild in bot.fetch_guilds(limit=100):
            async for member in guild.fetch_members(limit=150):
                if member.display_name == args[0]:
                    user_queried = member
        page = args[1]
    elif len(args) == 0:
        page = 1
    elif len(args) == 1 and not args[0].isnumeric():
        await ctx.send("Invalid arguments, please add a page number!")
        return
    else:
        page = args[0]
    numClips = user.get_num_clips(user_queried.id)
    clips = user.get_clips(user_queried.id)
    total_pages = math.ceil(numClips/5)

    if numClips == 0:
        await ctx.send("No Clips!")
        return


    if int(page) > total_pages:
        await ctx.send("Not that many pages!")
        return
    elif (int(page)*5) > numClips:
        numDisplay = 5 - ((int(page)*5)-numClips)
        start_val = int((int(page)-1)*5)
        end_val = int(start_val + numDisplay)
    else:
        start_val = int((int(page)-1)*5)
        end_val = int(start_val + 5)
    embed_title = user_queried.display_name + "'s Clips!"
    embed = discord.Embed(title=embed_title,
                      colour=0x00b0f4,
                      timestamp=datetime.now())

    #embed.set_author(name="Clip Manager")
    
    print(str(start_val) + " " + str(end_val))
    for i in range(start_val, end_val):
        url = clips[i]['link']
        title = clips[i]['title']
        embed.add_field(name="", value ="["+str(numClips-i)+") "+title+"]("+url+")", inline=False)

    #embed.set_thumbnail(url="https://i.pinimg.com/564x/8e/3e/ff/8e3eff7aa6f1147fabcc866666a6c22c.jpg")
    embed.set_thumbnail(url=user_queried.avatar)

    embed.set_footer(text="Page " + str(page) + "/" + str(total_pages),
                    icon_url="https://slate.dan.onl/slate.png")
    await ctx.send(embed=embed)

@bot.command()
async def remove(ctx, *args):
    if len(args) != 1:
        await ctx.send("Invalid Number of Arguments")
    if args[0].isnumeric() == False:
        await ctx.send("Argument is not numeric!")
    user_queried = ctx.author
    numClips = user.get_num_clips(user_queried.id)
    if int(args[0]) > int(numClips) or int(args[0]) < 1:
        await ctx.send("Invalid index!")
        return
    
    idx =  numClips - int(args[0])
    s3_link = user.remove_clip('clip-manager', user_queried.id, idx)
    await video.delete_video(s3_link)
    await ctx.send("Clip removed!")

    
    




@bot.command()
async def robertabot(ctx):
    embed = discord.Embed(title="Junioryang 27's Clips",
                        colour=0x00b0f4,
                        timestamp=datetime.now())

    embed.set_author(name="Clip Manager")

    embed.add_field(name="Valorant Ascent 5k",
                    value="https://d1iri5prxiem86.cloudfront.net/6d97d429-e4d5-4286-a0e3-3954a2c99e93.mp4", 
                    inline="false")
    embed.add_field(name="Clip 2: Valorant Ascent 4k",
                    value="https://d1iri5prxiem86.cloudfront.net/6d97d429-e4d5-4286-a0e3-3954a2c99e93.mp4",
                    inline="false")

    embed.set_thumbnail(url="https://pbs.twimg.com/media/Ez7a3GZWYAMMm2E.jpg")

    embed.set_footer(text="10/10 Bot",
                    icon_url="https://slate.dan.onl/slate.png")

    await ctx.send(embed=embed)


@bot.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')

@bot.command()
async def me(ctx):
    tempresponse = user.get_item('clip-manager', ctx.author.id)
    if tempresponse["numclips"] == 1: 
        await ctx.send(tempresponse['username'] + " " + "has " + str(tempresponse['numclips']) + " clip!")
    else:
        await ctx.send(tempresponse['username'] + " " + "has " + str(tempresponse['numclips']) + " clips!")


@bot.event
async def on_ready():
    guild_count = 0

    async for guild in bot.fetch_guilds(limit=100):
        print(guild.name)

        guild_count += 1

    print ("Clip Manager is in " + str(guild_count) + " guilds")


@bot.event

async def on_message(message):
    
    if "outplayed.tv" in message.content:
        contents = message.content.replace('\n',' ')
        contents = contents.split(" ")
        print(contents)

        filename = await video.download_file(contents[-1])
        contents.pop()
        title = " ".join(contents)
        await asyncio.sleep(5)
        if os.path.isfile(filename) == True:
            file_modified = str(message.author.id)+'/'+filename
            await video.upload_file(filename, file_modified, 'clip-manager')
            file_url= CLOUDFRONT_URL+"/"+file_modified
            await message.channel.send("Clip uploaded!")
            await asyncio.sleep(10)
            if user.check_user_in_table(message.author.id) == False:
                user.add_user(table_name, message.author.id, message.author.display_name)
            user.add_clip(table_name, message.author.id, title, file_url)
            path ='/'+filename
            clean.run_clean('./')
        else: 
            print("Error downloading Video")

    else: 
        await bot.process_commands(message)

            
bot.run(DISCORD_TOKEN)





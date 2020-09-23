from discord.ext import commands, tasks
import discord
import requests as req
import json
import datetime
import pathlib
import time



gameShorts = {"bedwars":["BED","BedWars","🛏️"],
            "murder_in_mineville":["MIMV", "Murder in Mineville","🔪"]}


def playerSpot(game,spot):
    return json.loads(req.get("http://api.hivemc.com/v1/game/%s/leaderboard/%s/%s"%(gameShorts[game.lower()][0],str(int(num)-1),num)).text)["leaderboard"][0]["username"]


def log( command, args, user , server ,failed = False ):
    with open(str(pathlib.Path(__file__).parent.absolute())+"/log_file.txt", "a+") as f:
        if not failed:
            f.write(('\n'+ str(datetime.datetime.now()) + '\n' + 'ran command ' +command + ' | by the user ' +str(user) +  ' | with the arguments: ' +str(args) + ' | on server: ' + str(server)))
            print('\n'+ str(datetime.datetime.now()) + '\n' + 'ran command ' +command + ' | by the user ' +str(user) +  ' | with the arguments: ' +str(args) + ' | on server: ' + str(server))
        else:
            f.write(('\n' + str(datetime.datetime.now()) + '\n' + 'failed to run command ' +command + ' | by the user ' +str(user) +  ' | with the arguments: ' +str(args) + ' | on server: ' + str(server)))
            print('\n' + str(datetime.datetime.now()) + '\n' + 'failed to run command ' +command + ' | by the user ' +str(user) +  ' | with the arguments: ' +str(args) + ' | on server: ' + str(server))


client = commands.Bot(command_prefix = "#")


#playerStats command: General stats of player in the server
@client.command()
async def playerStats(ctx, playerName):
    playerInfo = json.loads(req.get("https://api.hivemc.com/v1/player/"+playerName).text)

    toPrint = ""

    toPrint += "**🐝 Your HiveMC Stats 🐝**\n\n"
    toPrint += "**username:** "+playerInfo["username"] +' 🍯\n'
    toPrint += "**Rank:** "+playerInfo["rankName"] +' ✨\n'
    toPrint += "**Tokens:** "+str(playerInfo["tokens"]) +' 💲\n'
    toPrint += "**Medals:** "+str(playerInfo["medals"]) +' 🥇\n'
    toPrint += "**Last Seen:** "+time.asctime(time.gmtime(playerInfo["lastLogout"])) +' UTC ⏰\n'

    await ctx.message.channel.send(content = toPrint)

#playerStats command: General stats of player in the server
@client.command()
async def gameStats(ctx,game, playerName):
    if game.lower() in str(gameShorts).lower():
        playerInfo = json.loads(req.get("http://api.hivemc.com/v1/player/%s/%s"%(playerName,gameShorts[game.lower()][0])).text)
        gameEm = gameShorts[game.lower()][2]
        gameName = gameShorts[game.lower()][1]
        toPrint = '%s  **Your %s Stats**  %s \n\n'%(gameEm,gameName,gameEm)
        try: toPrint += "**Total Points:** %s 🌟 \n"%(playerInfo["total_points"])
        except: pass
        try: toPrint += "**Total Kills:** %s 🗡️\n"%(playerInfo["kills"])
        except: pass
        try: toPrint += "**Total Deaths:** %s ☠️\n"%(playerInfo["deaths"])
        except: pass
        try: toPrint += "**Wins:** %s 🏆\n"%(playerInfo["victories"])
        except: pass
        try: toPrint += "**Beds Destroyed:** %s 🛏️\n"%(playerInfo["beds_destroyed"])
        except: pass
        try: toPrint += "**Games Played:** %s 🕹️\n"%(playerInfo["games_played"])
        except: pass
        try: toPrint += "**Win Streak:** %s 🎳\n"%(playerInfo["win_streak"])
        except: pass
        try: toPrint += "**K/D Ratio:** %s ➗\n"%("%0.2f" % (playerInfo["kills"]/playerInfo["deaths"]))
        except: pass
        try: toPrint += "**W/L Ratio:** %s ➗\n"%("%0.2f" % (playerInfo["victories"]/(playerInfo["games_played"]-playerInfo["victories"])))
        except: pass

        if "Total Points" not in toPrint:
            await ctx.message.channel.send(content = "This player has no stats for this game.")
        else:
            await ctx.message.channel.send(content = toPrint)
    else: 
        await ctx.message.channel.send(content = "This game is either not supported or doesn't exist")



@client.command()
async def top10(ctx,game):
    if game.lower() in str(gameShorts).lower():
        gameEm = gameShorts[game.lower()][2]
        gameName = gameShorts[game.lower()][1]
        lb = json.loads(req.get("http://api.hivemc.com/v1/game/%s/leaderboard/0/10"%(gameShorts[game.lower()][0])).text)["leaderboard"]
        toPrint = '%s  **The Top #10 %s Players!**  %s \n\n'%(gameEm,gameName,gameEm)
        for i in range(10):
            clb = lb[i]
            toPrint += "**" + str(i+1) + ". " + clb["username"] + "**\n    **Points:** %s 🌟\n    **Winstreak:** %s 🎳 \n"%(clb['total_points'],clb["win_streak"])
        await ctx.message.channel.send(content = toPrint)
    else: 
        await ctx.message.channel.send(content = "This game is either not supported or doesn't exist")

@client.command()
async def spot(ctx,num,game):
    if game.lower() in str(gameShorts).lower():
        gameEm = gameShorts[game.lower()][2]
        gameName = gameShorts[game.lower()][1]
        lb = json.loads(req.get("http://api.hivemc.com/v1/game/%s/leaderboard/%s/%s"%(gameShorts[game.lower()][0],str(int(num)-1),num)).text)["leaderboard"]
        toPrint = '%s  **The Top #%s %s Player!**  %s \n\n'%(gameEm,num,gameName,gameEm)
        clb = lb[0]
        toPrint += "**" + num + ". " + clb["username"] + "**\n    **Points:** %s 🌟\n    **Winstreak:** %s 🎳 \n"%(clb['total_points'],clb["win_streak"])
        await ctx.message.channel.send(content = toPrint)
    else: 
        await ctx.message.channel.send(content = "This game is either not supported or doesn't exist")



@client.command()
async def top5(ctx,game):
    if game.lower() in str(gameShorts).lower():
        gameEm = gameShorts[game.lower()][2]
        gameName = gameShorts[game.lower()][1]
        lb = json.loads(req.get("http://api.hivemc.com/v1/game/%s/leaderboard/0/10"%(gameShorts[game.lower()][0])).text)["leaderboard"]
        toPrint = '%s  **The Top #5 %s Players!**  %s \n\n'%(gameEm,gameName,gameEm)
        for i in range(5):
            clb = lb[i]
            toPrint += "**" + str(i+1) + ". " + clb["username"] + "**\n    **Points:** %s 🌟\n    **Winstreak:** %s 🎳 \n"%(clb['total_points'],clb["win_streak"])
        await ctx.message.channel.send(content = toPrint)
    else: 
        await ctx.message.channel.send(content = "This game is either not supported or doesn't exist")


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    try:
        await ctx.channel.purge(limit = amount + 1)
        log('clear',amount+1,ctx.author,ctx.message.guild)
    except:
        log('clear',amount+1,ctx.author,ctx.message.guild,True)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason = None):
    try:
        await member.kick(reason = reason)
        log('kick',[member,reason],ctx.author,ctx.message.guild)
    except:
        log('kick',[member,reason],ctx.author,ctx.message.guild,True)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason = None):
    try:
        await member.ban(reason = reason)
        log('ban',[member,reason],ctx.author,ctx.message.guild)
    except:
        log('ban',[member,reason],ctx.author,ctx.message.guild,True)

@client.event
async def on_ready():
    print("bot is ready")
    await client.change_presence(activity=discord.Game(name=" on HiveMC 🐝"))

client.run(  open(str(pathlib.Path(__file__).parent.absolute())+"token.txt","r").read()  )

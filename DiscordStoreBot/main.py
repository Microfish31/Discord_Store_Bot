from discord.ext import commands
from discord_slash import SlashCommand
import random
#import os
import json
import keep_alive

# command  
# $search_store 
# $add_store  arg
# $random_store
# $delete_store arg

#data_path = os.getcwd() + "\\data"
#.........................................................
data_path = './data/discord_data.txt'

with open('setting.json','r',encoding='utf8') as f :
     setting = json.load(f)

bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True)

#..........................................................

#當機器人完成啟動時
@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)

#..............................................................
@slash.slash(description="Bot Latency")
async def ping(ctx):
    await ctx.send(f"Speed - {round(bot.latency*1000)} ms")

@slash.slash(description="To search some stores.")
async def search_store(ctx):
    get_all_stores = s_store()
    await ctx.send(get_all_stores)

@slash.slash(description="To add a store.")
async def add_store(ctx,name):
    check = a_store(name)
    if check == False :
      with open(data_path,'a') as f:
          f.write(name+"\n")
      await ctx.send(f"已添加 {name}")
    else :
      await ctx.send(f"加過了啦幹")

@slash.slash(description="To choose a store randomly.")
async def random_store(ctx):
    get_store = r_store()
    if get_store != "" :
        await ctx.send(get_store)

@slash.slash(description="To delete the choosed store.")
async def delete_store(ctx,name):
    if d_store(name) == 1 :
        await ctx.send(f"已刪除 {name}")
    else:
        await ctx.send(f"不存在 {name}")
#...............................................................

#...............................................................
def s_store() :
    with open(data_path,'r', encoding="utf8") as f:
        content_list = f.read()
    return content_list

def a_store(get_store) :
    check = False
    with open(data_path,'r', encoding="utf-8") as f:
        line = f.readline()
        while line:
            if line.strip('\n') == get_store:
               check = True
               break
            line = f.readline()

    return check

def r_store(): 
    a = []
    with open(data_path,'r', encoding="utf-8") as f:
        line = f.readline()
        while line:
            a.append(line)
            line = f.readline()
    return a[random.randint(0,len(a)-1)]

def d_store(store_name): 
    check = 0
    with open(data_path,'r+', encoding="utf-8") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i.strip('\n') != store_name:
                f.write(i)
            else :
               check = 1
        f.truncate()
    return check

#......................................................    

keep_alive.keep_alive()

#TOKEN
bot.run(setting['Token']) 
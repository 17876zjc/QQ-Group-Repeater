from aiocqhttp import CQHttp
import os
import random
from click import command

from sympy import use
from Repeater import Repeater
import logging

import time
from util import load_json, purgeMsg
from datetime import timezone

from queue import Queue
from pytz import timezone
from crontab import CronTab

import wgmanager

from bot_p import bot

used_timezone=timezone('Asia/Shanghai')

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          'coolq.log'),
    filemode='w+')

#bot = CQHttp(api_root='http://127.0.0.1:5700/')

GroupDict = dict()
SETTINGS = load_json('settings.json')
REPLY = load_json('data/reply.json')
msgQueue = Queue()

# app = bot.server_app
# @app.route('/danmu/coolq')
# async def danmu():
#     if request.remote_addr and request.remote_addr != '127.0.0.1':
#         return None
#     re = []
#     while not msgQueue.empty():
#         re.append(msgQueue.get())
#     return jsonify(re)


@bot.on_message('private')
async def handle_private(context):
    await bot.send(context, message=context['message'])
    if context['user_id'] in SETTINGS['ADMIN']:
        for group_id in SETTINGS['REPOST_GROUP']:
            await bot.send({'group_id': group_id}, message=context['message'])


@bot.on_message('group')
async def handle_msg(context):
    groupId = context['group_id']
    """if groupId in SETTINGS['DANMU_GROUP']:
        print(123)
        msgQueue.put({
            'sender': context['user_id'],
            'msg': context['message']
            # 'msg': purgeMsg(context['message'])
        })"""
    if groupId not in SETTINGS['ALLOW_GROUP']:
        return
    global GroupDict
    try:
        if (GroupDict.get(groupId) == None):
            GroupDict[groupId] = Repeater()
        re = await GroupDict[groupId].responseMsg(context)
        print({"msg": context['message'], "ans": re})
        await bot.send({'group_id': groupId}, message=re) if (len(re) > 0) else 0
    except Exception as e:
        print(str(e))
        print({"msg": context['message'], "ans": "ERROR"})
        logging.exception(e)


@bot.on_notice('group_increase')
async def handle_group_increase(context):
    if context['group_id'] not in SETTINGS['ALLOW_GROUP']:
        return
    re = random.choice(REPLY['on_group_increase'])
    await bot.send(context, message=re, auto_escape=True)


@bot.on_request('group', 'friend')
async def handle_group_request(context):
    return {'approve': True}


async def send_early_msg():
    #await asyncio.sleep(int(random.random() * 60 * 60) + 900)
    #time_format = '%Y-%m-%d %H:%M:%S'
    #bj_offset = timezone(timedelta(hours=8))
    #bj_datetime = datetime.now(bj_offset)
    time.sleep(15) 
    ###
    print("In func early_msg")
    ###
    re = random.choice(REPLY['on_early'])
    for group_id in SETTINGS['MEMTION_GROUP']:
        await bot.send({'group_id': group_id}, message=re)


async def send_new_day_msg():
    for group_id in SETTINGS['MEMTION_GROUP']:
        re = random.choice(REPLY['on_new_day'])
        await bot.send({'group_id': group_id}, message=re)

def sche():
    print("Runnig Sche")
    cron  = CronTab(user = True)
    cron.remove_all()
    #job1 = cron.new(command = 'sudo python3 ~/QQ/QQ-Group-Repeater/dailysche.py',comment = 'send test')
    #job1.setall('0 20 * * *')

    #job2 = cron.new(command = 'sudo python ~/QQ/QQ-Group-Repeater/dailysche.py',comment = 'send test')
    #job2.setall('0 8 * * *')
    
    job3 = cron.new(command = 'sudo python3 ~/QQ/QQ-Group-Repeater/wgsche.py >> wgout.txt  2>&1',comment = 'wg')
    job3.setall('*/5 * * * *')

    job4 = cron.new(command = 'sudo python3 ~/QQ/QQ-Group-Repeater/thresultsche.py >> thout.txt  2>&1',comment = 'th')
    job4.setall('*/5 * * * *')

    job5 = cron.new(command = 'sudo rm ~/*.txt')
    job5.setall('0 0 * * *')

    cron.write()
    print("Starting schedule")


if __name__ == '__main__':
    #wg.wgsync()
    #sche()
    try:
        wgmanager.wgmanager = wgmanager.WgManager()
        
        bot.run(host='0.0.0.0', port=8090)
        print("Ready to end.")
        wgmanager.wgmanager.kill()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        wgmanager.wgmanager.kill()
    except Exception as e:
        print("Exception")
        print(str(e))
        wgmanager.wgmanager.kill()

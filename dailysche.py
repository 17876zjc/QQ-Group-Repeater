import coolq
import asyncio

import random
import json
from Repeater import aioGet
from Bot import Bot
import time

async def dailySetu():
    print("In sending early day msg")
    res = ""
    try:
        tag = random.choice(
                        ['breasts', 'stockings', 'thighhighs', 'cleavage'])
        url = "https://konachan.net/post.json?" + \
            f"tags={tag}&page={random.randint(1, 100)}"
        tmpJson = json.loads(await aioGet(url))
        urls = [
            item['file_url'] for item in tmpJson
            if item['rating'] == 's'
        ]
        res = random.choice(urls)
    except:
        re = Bot.REPLY.get("get_image_failed")
        return random.choice(re) if re else ''

    localtime = time.localtime(time.time())
    msg = ""
    if(abs(localtime.tm_hour - 8) <= 1):
        msg = "早八时间到啦! 早起的人才有涩图看哦\n"
    else:
        msg = "辛苦一天啦, 来看看涩图吧\n"
    for group_id in coolq.SETTINGS['MEMTION_GROUP']:
        await coolq.bot.send({'group_id': group_id}, message=(msg+f"[CQ:image,file={res}]"))

loop = asyncio.get_event_loop()
result = loop.run_until_complete(dailySetu())
loop.close()

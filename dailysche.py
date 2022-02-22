import coolq
import asyncio

async def dailysche():
    print("In sending early day msg")
    for group_id in coolq.SETTINGS['MEMTION_GROUP']:
        await coolq.bot.send({'group_id': group_id}, message="消息测试")

loop = asyncio.get_event_loop()
result = loop.run_until_complete(dailysche())
loop.close()

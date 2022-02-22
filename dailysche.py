import coolq

print("In sending early day msg")
for group_id in coolq.SETTINGS['MEMTION_GROUP']:
    coolq.bot.send({'group_id': group_id}, message="消息测试")
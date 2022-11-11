from aiocqhttp import CQHttp
bot = None

def init():
    bot = CQHttp(api_root='http://127.0.0.1:5700/')
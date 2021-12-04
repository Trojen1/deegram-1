import shutil, psutil
import time

from telethon import Button, events
from telethon.events import NewMessage, StopPropagation

from . import bot, botStartTime, logger, plugins, OWNER_ID
from .utils import translate, fetch
from .utils.bot_utils import get_readable_file_size, get_readable_time

plugins.load()


@bot.on(NewMessage(pattern='/help'))
async def get_help(event: NewMessage.Event):
    await event.reply(translate.HELP_MSG)


@bot.on(NewMessage(pattern='/info'))
async def info(event: NewMessage.Event):
    await event.reply(translate.INFO_MSG)
    raise StopPropagation


@bot.on(NewMessage(pattern='/log', from_users=OWNER_ID))
async def log(event: NewMessage.Event):
    await event.reply(file='deegram.log')
    raise StopPropagation


@bot.on(NewMessage(pattern='/stats'))
async def stats(event: NewMessage.Event):
    current_time = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    upload = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    download = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    await event.reply(translate.STATS_MSG.format(current_time, total, used, free, upload, download, cpu, ram, disk))
    raise StopPropagation



with bot:
    bot.run_until_disconnected()
    logger.info('Bot stopped')
    bot.loop.run_until_complete(fetch.session.close())

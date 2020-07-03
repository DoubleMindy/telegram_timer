
import ptbot
import os
from pytimeparse import parse

TOKEN=os.getenv("TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
is_first_iteration = True
time = 0

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify_progress(secs_left, message_id):
	global is_first_iteration, time
	if is_first_iteration:
		is_first_iteration = False
		time = secs_left
	bot.update_message(CHAT_ID, message_id, render_progressbar(time, time-secs_left))

def notify():
	bot.send_message(CHAT_ID, "Время вышло!")

def say_hello(text):
	parsed_time = parse(text)
	bot.create_timer(parsed_time, notify)
	message_id = bot.send_message(CHAT_ID, "Таймер запущен на {} секунд".format(parsed_time))
	bot.create_countdown(parsed_time, notify_progress, message_id = message_id)

bot = ptbot.Bot(TOKEN)
bot.send_message(CHAT_ID, "Привет! На сколько запустить таймер?")
bot.reply_on_message(say_hello)

bot.run_bot()

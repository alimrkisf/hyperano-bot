
import os
import telebot
from flask import Flask, request

TOKEN = os.environ['My_Token']

bot = telebot.TeleBot(TOKEN, parse_mode=None)

server = Flask(__name__)

# # Bot commands
# @bot.message_handler(commands = 'start')
# def start(msg):
#   bot.reply_to(msg, 'این بات در دست راه اندازی است. \nاز صبر و شکیبایی شما مچکریم')

# @bot.message_handler(commands = 'help')
# def help(msg):
#   bot.reply_to(msg, '')

# # Auto responcive
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)

# #Polling
# # bot.polling()
# bot.infinity_polling()







"""
This is a detailed example using almost every command of the API
"""

import time

from telebot import types

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'دستور شروع خرید',
    'help'        : 'راهنمای استفاده از ربات',
    'menu'        : 'باز کردن منوی محصولات',
    'website'     : 'رفتن به سایت هایپرانو',
    'search'      : 'جستوجوی محصولات'
    # 'sendLongText': 'A test using the \'send_chat_action\' command',
    # 'getImage'    : 'A test using multi-stage messages, custom keyboard, and media sending'
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('Mickey', 'Minnie')

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "سلام به ربات هایپرانو خوش آمدید !")
        bot.send_message(cid, "اطلاعات شما با موفقیت ثبت شد.")
        # command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "با سلام مجدد\nبه ربات هایپرانو خوش آمدید\nاطلاعات شما قبلا در ربات ما ثبت شده است.")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "دستورات زیر در دسترس هستند:  \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# menu command
@bot.message_handler(commands=['menu'])
def command_menu(m):
    cid = m.chat.id
    bot.send_message(cid, 'فهرست کامل محصولات به زودی قرار می گیرند.')

# website command
@bot.message_handler(commands=['website'])
def command_website(m):
    cid = m.chat.id
    bot.send_message(cid, 'برای رفتن به وبسایت فروشگاهی هایپرانو لینک زیر را دنبال کنید:\nhyperano.ir')

# search command
@bot.message_handler(commands=['search'])
def command_serach(m):
    cid = m.chat.id
    bot.send_message(cid, 'با رفتن به سایت hyperano.com در قسمت جستجو محصول مورد نظر خود را بیابید')

# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your image now", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/getImage" command, process the answer
# @bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
# def msg_image_select(m):
#     cid = m.chat.id
#     text = m.text

#     # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
#     bot.send_chat_action(cid, 'typing')

#     if text == 'Mickey':  # send the appropriate image based on the reply to the "/getImage" command
#         bot.send_photo(cid, open('rooster.jpg', 'rb'),
#                        reply_markup=hideBoard)  # send file and hide keyboard, after image is sent
#         userStep[cid] = 0  # reset the users step back to 0
#     elif text == 'Minnie':
#         bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
#         userStep[cid] = 0
#     else:
#         bot.send_message(cid, "Please, use the predefined keyboard!")
#         bot.send_message(cid, "Please try again")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "دستور \"" + m.text + "\"یافت نشد. برای باز شدن راهنمای ربات از دستور /help استفاده کنید.")


# bot.infinity_polling()

@server.routel('/'+TOKEN, methods=['POST'])
def getMessage():
  bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
  return "!", 200

@server.routel("/")
def webhook():
  bot.remove_webhook()
  bot.set_webhook(url='https://afternoon-wave-36138.herokuapp.com/' + TOKEN)
  return "!", 200

if __name__ = "__main__":
  server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

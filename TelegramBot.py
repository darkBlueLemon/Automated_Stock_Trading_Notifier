import os
import telebot

API_KEY = "6695354276:AAFODyHzQdM_s6MT3i4sMIJABw1VHOD05MQ"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Gotcha")


@bot.message_handler(commands=['id'])
def hello(message):
    bot.send_message(message.chat.id, f"{message.chat.id}")


@bot.message_handler(commands=['test'])
def trigger(id, time):
    bot.send_message(id, f"{time}")


# bot.polling()

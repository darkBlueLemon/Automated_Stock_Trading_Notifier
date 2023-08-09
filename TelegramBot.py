import telebot

API_KEY = "6695354276:AAFODyHzQdM_s6MT3i4sMIJABw1VHOD05MQ"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f"{message.chat.id} -> add this to the chat_ids list")


@bot.message_handler(commands=['trigger'])
def trigger(chat_ids, text=''):
    if not chat_ids or not text:
        print("No chat IDs to send messages to.")
        return

    for chat_id in chat_ids:
        bot.send_message(chat_id, f"{text}")


if __name__ == "__main__":
    # Start the bot's polling
    bot.polling()

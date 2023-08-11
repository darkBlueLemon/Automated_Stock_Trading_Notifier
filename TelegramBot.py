import telebot
import threading
import os
import signal
import psutil
import subprocess
import config

API_KEY = config.API_KEY

bot = telebot.TeleBot(API_KEY)
authenticated_users = {}
flag = "0"


@bot.message_handler(commands=['hibernate'])
def request_password(message):
    global flag
    authenticated_users[message.chat.id] = False
    bot.send_message(message.chat.id, "Please enter the password to hibernate:")
    flag = "hibernate"


@bot.message_handler(commands=['stop_code'])
def request_password(message):
    global flag
    authenticated_users[message.chat.id] = False  # Set authentication status to False
    bot.send_message(message.chat.id, "Please enter the password to stop the code:")
    flag = "stop_code"


@bot.message_handler(
    func=lambda message: message.chat.id in authenticated_users and not authenticated_users[message.chat.id])
def check_password(message):
    if message.text == config.authentication_password:  # Replace "your_password_here" with the actual password
        authenticated_users[message.chat.id] = True  # Set authentication status to True
        if flag == "hibernate":
            bot.send_message(message.chat.id, "Password accepted. Sending hibernate signal...")
            subprocess.run(["shutdown", "/h"])
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if 'python' in process.info['name'].lower():
                    os.kill(process.info['pid'], signal.SIGTERM)
        else:
            bot.send_message(message.chat.id, "Password accepted. Sending stop signal...")
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if 'python' in process.info['name'].lower():
                    os.kill(process.info['pid'], signal.SIGTERM)
    elif message.text == "/start":
        bot.send_message(message.chat.id,
                         f"<b>Commands</b>\n/stop_code - terminates the program on the server\n/hibernate - "
                         f"terminates the program and hibernates the server\n/help - prints this message\n\n"
                         f"{message.chat.id} -> Add this to chat_ids\n\n",
                         parse_mode="HTML")
    elif message.text == "/help":
        bot.send_message(message.chat.id,
                         "<b>Commands</b>\n/stop_code - terminates the program on the server\n/hibernate - terminates "
                         "the program and hibernates the server\n/help - prints this message",
                         parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Incorrect password. Please try again.")


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f"<b>Commands</b>\n/stop_code - terminates the program on the "
                                      f"server\n/hibernate - terminates the program and hibernates the serve"
                                      f"r\n/help - prints this message\n\n{message.chat.id} -> Add this to "
                                      f"chat_ids\n\n", parse_mode="HTML")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "<b>Commands</b>\n/stop_code - terminates the program on the server\n/hibernate "
                                      "- terminates the program and hibernates the server\n/help - prints this "
                                      "message", parse_mode="HTML")


@bot.message_handler(commands=['trigger'])
def trigger(chat_ids, text=''):
    if not chat_ids or not text:
        print("No chat IDs to send messages to.")
        return

    for chat_id in chat_ids:
        bot.send_message(chat_id, f"{text}")


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(message.chat.id, "Unknown command. Here are the available commands:\n"
                                      "/stop_code - terminates the program on the server\n"
                                      "/hibernate - terminates the program and hibernates the server\n"
                                      "/help - prints this message")


def polling_thread():
    bot.polling(none_stop=True, interval=1, timeout=20)


if __name__ == "__main__":
    print("Bot is now running in the background.")
    bot.polling()
else:
    polling_thread = threading.Thread(target=polling_thread)
    polling_thread.daemon = True
    polling_thread.start()
    print("Bot is now running in the background.")



# https://economictimes.indiatimes.com/marketstats/pid-1004,exchange-50,sortby-percentChange,sortorder-desc,indexid-13602,company-true,indexname-Nifty%20200.cms

import pyautogui
import easyocr
import time
import datetime
from datetime import datetime
from TelegramBot import trigger
import config
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')


def get_region_coordinates():
    try:
        global x1, y1, x2, y2, x3, y3, x4, y4
        with open('coordinates.txt', 'r') as file:
            line = file.readline().strip()

        coordinates = list(map(int, line.split()))

        if len(coordinates) == 8:
            x1, y1, x2, y2, x3, y3, x4, y4 = coordinates
        else:
            print("Invalid number of coordinates.")
    except Exception as e:
        logging.error(f"An error occurred in get_region_coordinates(): {e}")
        traceback.print_exc()


# Handles file handling
def write_to_disk(signal):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    with open("Signals.csv", "a") as file:
        file.write(f"{formatted_datetime}, {signal}\n")


# Takes a screenshot of the first 6 stocks and returns a list
def take_screenshot_and_read_words():
    try:
        # im = pyautogui.screenshot(region=(600, 505, 177, 388))
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))

        im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\ss_name.png")

        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext('ss_name.png')

        words_with_non_alpha = [item[1] for item in result]
        cleaned_words = []

        for word in words_with_non_alpha:
            cleaned_word = "".join(char if char.isalpha() or char.isspace() else "" for char in word)
            cleaned_words.append(cleaned_word)

        return cleaned_words
    except Exception as e:
        logging.error(f"An error occurred in take_screenshot_and_read_words(): {e}")
        traceback.print_exc()


# Takes a screenshot of the first 6 stocks-prices and returns a list
def take_screenshot_and_read_numbers():
    try:
        # im = pyautogui.screenshot(region=(1024, 505, 93, 385))
        im = pyautogui.screenshot(region=(x3, y3, x4, y4))

        im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\ss_price.png")

        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext('ss_price.png')

        number_list = [item[1] for item in result]
        cleaned_numbers = []

        for word in number_list:
            cleaned_number = "".join(char if char.isdigit() or char == '.' else "" for char in word)
            cleaned_numbers.append(cleaned_number)

        return cleaned_numbers

    except Exception as e:
        logging.error(f"An error occurred in take_screenshot_and_read_numbers(): {e}")
        traceback.print_exc()


# Adds and checks if any current holding has dropped by $risk_percentage
def update_holdings(current_words, numbers):
    try:
        global holdings
        checked_stocks = set()
        for word in current_words:
            try:
                if word in holdings:
                    index_holdings = current_words.index(word)
                    num = float(numbers[index_holdings])
                    prev_num = float(holdings[word])
                    if num <= prev_num - config.lower_sell_limit or num >= prev_num + config.upper_sell_limit:
                        trigger(config.chat_ids, f"SELL {word} at {num}%")
                        print(f"SELL {word} at {num}%")
                        write_to_disk(f"SELL, {word}, {num}%")
                        del holdings[word]
                    else:
                        checked_stocks.add(word)
            except (IndexError, ValueError):
                print(f"Error: Unable to find the price for {word}.")

        temp = set()
        for word in holdings:
            if word not in checked_stocks:
                trigger(config.chat_ids, f"MISSING STOCK -> SELL {word}")
                print(f"MISSING STOCK -> SELL {word}")
                write_to_disk(f"SELL, {word}, NA")
                temp.add(word)

        for word in temp:
            del holdings[word]

        print(f"Holdings:\n{holdings}")

    except Exception as e:
        logging.error(f"An error occurred in update_holdings(): {e}")
        traceback.print_exc()


def time_keeper():
    # Specify the target time
    target_time = datetime.strptime(config.start_time, "%Y-%m-%d %H:%M:%S")

    # Get the current time
    current_time = datetime.now()

    # Calculate the time difference
    time_difference = target_time - current_time

    # Convert the time difference to seconds
    time_difference_seconds = time_difference.total_seconds()

    # If the target time is in the past, adjust the time difference for the next day
    if time_difference_seconds < 0:
        return
        # time_difference_seconds += 24 * 60 * 60  # Add 24 hours in seconds

    # Calculate days, hours, minutes, and seconds
    days, seconds = divmod(time_difference_seconds, 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)

    print(f"Time difference: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

    # Sleep until the target time
    time.sleep(time_difference_seconds)

    # Code execution will continue after the specified target time
    print("Time to wake up!")


holdings = {}


def main():
    try:
        time_keeper()
        previous_words = []
        previous_words_top = []
        first_screenshot_taken = False
        chat_ids = config.chat_ids
        get_region_coordinates()

        while True:

            current_words = take_screenshot_and_read_words()
            numbers = take_screenshot_and_read_numbers()

            current_words_top = current_words[:config.buy_window_size]

            if first_screenshot_taken:
                for word in current_words_top:
                    if word not in previous_words_top:
                        try:
                            index = current_words.index(word)
                            holdings[word] = numbers[index]
                            trigger(chat_ids, f"BUY {word} at {numbers[index]}%")
                            print(f"BUY {word} at {numbers[index]}%")
                            write_to_disk(f"BUY, {word}, {numbers[index]}%")
                        except IndexError:
                            print("Index OFB")
                update_holdings(current_words, numbers)
            else:
                first_screenshot_taken = True

            previous_words = current_words
            previous_words_top = current_words_top
    except Exception as e:
        logging.error(f"An error occurred in main(): {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()

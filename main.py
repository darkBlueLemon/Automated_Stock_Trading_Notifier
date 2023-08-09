# https://economictimes.indiatimes.com/marketstats/pid-1004,exchange-50,sortby-percentChange,sortorder-desc,indexid-13602,company-true,indexname-Nifty%20200.cms

import pyautogui
import easyocr
import time
import datetime
from TelegramBot import trigger

def get_region_coordinates():
    global x1, y1, x2, y2, x3, y3, x4, y4
    with open('coordinates.txt', 'r') as file:
        line = file.readline().strip()

    coordinates = list(map(int, line.split()))

    if len(coordinates) == 8:
        x1, y1, x2, y2, x3, y3, x4, y4 = coordinates
    else:
        print("Invalid number of coordinates.")


# Handles file handling
def write_to_disk(signal):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    with open("Signals.csv", "a") as file:
        file.write(f"{formatted_datetime}, {signal}\n")
    file.close()


# Takes a screenshot of the first 6 stocks and returns a list
def take_screenshot_and_read_words():
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


# Takes a screenshot of the first 6 stocks-prices and returns a list
def take_screenshot_and_read_numbers():
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


# Adds and checks if any current holding has dropped by $risk_percentage
def update_holdings(current_words, numbers):
    global holdings
    checked_stocks = set()
    for word in current_words:
        try:
            if word in holdings:
                index = current_words.index(word)
                num = float(numbers[index])
                prev_num = float(holdings[word])
                if num <= prev_num - risk_percentage or num >= prev_num + 1.0:
                    trigger(chat_ids, f"SELL {word} at {num}%")
                    print(f"SELL {word} at {num}%")
                    write_to_disk(f"SELL, {word}, {num}%")
                    del holdings[word]
                else:
                    checked_stocks.add(word)
        except (IndexError, ValueError):
            print(f"Error: Unable to find the number for {word}.")

    temp = set()
    for word in holdings:
        if word not in checked_stocks:
            trigger(chat_ids, f"MISSING STOCK -> SELL {word}")
            print(f"MISSING STOCK -> SELL {word}")
            write_to_disk(f"SELL, {word}, NA")
            temp.add(word)

    for word in temp:
        del holdings[word]

    print(f"Holdings:\n{holdings}")


previous_words = []
holdings = {}
first_screenshot_taken = False
risk_percentage = 0.5
chat_ids = [1763559069, 6273784818, 5087400987]
get_region_coordinates()


while True:

    start_time = time.time()
    current_words = take_screenshot_and_read_words()
    numbers = take_screenshot_and_read_numbers()

    new_words = [word for word in current_words if word not in previous_words]
    if first_screenshot_taken:
        if new_words:
            for word in new_words:
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

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken:.2f} seconds")

import pyautogui
import easyocr
import time


def take_screenshot_and_read_words():
    im = pyautogui.screenshot(region=(600, 341, 177, 388))
    im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\ss_name.png")

    reader = easyocr.Reader(['en'])
    result = reader.readtext('ss_name.png')

    words = [item[1] for item in result]
    return words


def take_screenshot_and_read_numbers():
    im = pyautogui.screenshot(region=(1024, 345, 93, 385))
    im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\ss_price.png")

    reader = easyocr.Reader(['en'])
    result = reader.readtext('ss_price.png')

    numbers = [item[1] for item in result]
    return numbers


previous_words = []
holdings = []
first_screenshot_taken = False

while True:
    time.sleep(1)

    start_time = time.time()
    current_words = take_screenshot_and_read_words()
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken} seconds")

    new_words = [word for word in current_words if word not in previous_words]
    if first_screenshot_taken:
        if new_words:
            print("New words detected:")
            numbers = take_screenshot_and_read_numbers()
            for word in new_words:
                print(word)
                index = current_words.index(word)
                print(numbers[index])
    else:
        first_screenshot_taken = True

    previous_words = current_words

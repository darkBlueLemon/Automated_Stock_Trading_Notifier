import pyautogui
import easyocr
import time
def take_screenshot_and_read_words():
    im = pyautogui.screenshot(region=(251, 236, 449, 442))
    im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\screenshot.png")

    reader = easyocr.Reader(['en'])
    result = reader.readtext('screenshot.png')

    words = [item[1] for item in result]
    return words


previous_words = []

while True:
    time.sleep(1)

    current_words = take_screenshot_and_read_words()

    new_words = [word for word in current_words if word not in previous_words]
    if new_words:
        print("New words detected:")
        for word in new_words:
            print(word)

    previous_words = current_words




# import pyautogui
# import easyocr
# import time
#
# time.sleep(2)
#
# im = pyautogui.screenshot(region=(180, 220, 280, 400))
# im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\screenshot.png")
#
# reader = easyocr.Reader(['en'])
# result = reader.readtext('screenshot.png')
#
# words = [item[1] for item in result]
# for word in words:
#     print(word)
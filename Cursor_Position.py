from pynput.mouse import Listener

flag = False
temp = 0
temp2 = 0


def on_right_click(x, y, button, pressed):
    global flag, temp, temp2
    if pressed and button == button.right:
        with open("coordinates.txt", "a") as f:
            if not flag:
                f.write(f"{x} {y} ")
                flag = True
                temp = x
                temp2 = y
            else:
                f.write(f"{x - temp} {y - temp2} ")
                print(f"Bottom Left at X: {x}, Y: {y}")
                return False
        print(f"Top Right at X: {x}, Y: {y}")


def main():
    with Listener(on_click=on_right_click) as listener:
        listener.join()


if __name__ == "__main__":
    print("Right click to capture coordinates\nOnce for the Stock Names and once for Change%\n1. Top Left\n2. Bottom Right")
    open("coordinates.txt", "w")
    main()
    flag = False
    main()

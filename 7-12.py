import tkinter
from tkinter import ttk
import time


def say_hello():
    time.sleep(10)
    print("Hello there!")


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Hello world app")
    window.geometry("200x100")

    hello_button = ttk.Button(window, text="Say hello", command=say_hello)
    hello_button.pack()

    window.mainloop()

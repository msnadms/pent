import threading
import tkinter as tk
import win32api as wp
import sys
import ctypes
import main as m

MHEIGHT = wp.GetSystemMetrics(1)
MWIDTH = wp.GetSystemMetrics(0)
STOP = False


class PentOverlay:

    def __init__(self):
        self.root = tk.Tk()
        self.all_widgets = []

        self.button_settings = tk.Button(
            self.root,
            text='Settings',
            font=('Consolas', '14'),
            fg='blue',
            bg='#f7f7f7',
            relief='flat'
        )
        self.button_email = tk.Button(
            self.root,
            text='EMail',
            font=('Consolas', '14'),
            fg='blue',
            bg='#f7f7f7',
            relief='flat'
        )
        self.button_showdt = tk.Button(
            self.root,
            text='Desktop',
            font=('Consolas', '14'),
            fg='blue',
            bg='#f7f7f7',
            relief='flat'
        )

        self.button_settings.grid(row=0, column=0)
        self.button_email.grid(row=1, column=0)
        self.button_showdt.grid(row=2, column=0)
        self.all_widgets.append(self.button_settings)
        self.all_widgets.append(self.button_email)
        self.all_widgets.append(self.button_showdt)
        self.root.configure(background='grey19')
        self.root.wm_attributes('-transparentcolor', 'grey19')
        self.root.overrideredirect(True)
        self.root.geometry(f'{MWIDTH // 2 - 10}x{MHEIGHT - 10}+5+5')
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def forget_all(self):
        for widget in self.all_widgets:
            widget.grid_forget()

    def remember_all(self):
        for widget in self.all_widgets:
            widget.grid()

    def run(self):
        while not STOP:
            self.root.update_idletasks()
            self.root.update()
        # self.root.mainloop()


def main():
    app = PentOverlay()
    app.run()


if __name__ == "__main__":
    main()

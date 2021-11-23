import tkinter as tk
import win32api as wp

MHEIGHT = wp.GetSystemMetrics(1)
MWIDTH = wp.GetSystemMetrics(0)


class PentOverlay:

    def __init__(self):
        self.root = tk.Tk()

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

        self.button_settings.grid(row=0, column=0)
        self.button_email.grid(row=0, column=1)
        self.root.configure(background='grey19')
        self.root.wm_attributes('-transparentcolor', 'grey19')
        self.root.overrideredirect(True)
        self.root.geometry(f'{MWIDTH - 10}x{MHEIGHT // 2 - 10}+5+5')
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def run(self):
        self.root.mainloop()


def stop():
    pass


def main():
    app = PentOverlay()
    app.run()


if __name__ == "__main__":
    main()

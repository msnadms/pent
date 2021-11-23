import tkinter as tk


def launch_gui():

    window = tk.Tk()

    frame_left = tk.Frame()
    frame_left.pack(side=tk.LEFT)
    frame_right = tk.Frame()
    frame_right.pack(side=tk.RIGHT)

    title = tk.Label(master=frame_left, text="P_ENT")
    title.pack()

    enter_pent = tk.Button(master = frame_right, text="Deploy")
    enter_pent.pack()

    window.mainloop()


def main():
    launch_gui()


if __name__ == "__main__":
    main()



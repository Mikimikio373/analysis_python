import tkinter as tk

def text_print():
    print('test')

root = tk.Tk()
root.geometry("400x300")

input_box = tk.Entry(width=40)
input_box.place(x=10, y=10)


run_button = tk.Button(root, text='Run', command=text_print)
run_button.place(x=160, y=40)

statusbar = tk.Label(root, text='test', bd=1, relief=tk.SUNKEN, anchor=tk.W)
statusbar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
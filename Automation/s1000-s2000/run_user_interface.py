from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from test_controller import run_controller

def click():
    if type_var.get() == "":
        print("Select a system to test!")
    else:
        root.destroy()
        run_controller(type_var.get(), int(thread_count.get()))

def change_button_text ():
    run_button.configure(text=f"Run Tests for {type_var.get()}")

root = ttk.Window(themename="darkly")
root.geometry("750x500")
width=750
height=500

root.title ("LPSD Tester")
root.resizable(False, False)

type_var = StringVar()
thread_count = StringVar()

for i in range(2):
    rb = ttk.Radiobutton(root, text=f"S{i+1}000", variable=type_var, value=f"S{i+1}000", bootstyle="light-outline toolbutton", command=change_button_text)
    rb.place(relx=1/8, rely=(1+i)/9 + 1/height, width= 2 * width/8, height=height/9 - 2)

thread_count_dropdown = ttk.Combobox(root, width=1, textvariable=thread_count, state=READONLY, bootstyle=LIGHT)
thread_count_dropdown['values'] = ('1','2','3','4')
thread_count_dropdown.place(relx=6/8, rely=1.75/9, width=width/8, height=30)
thread_count_dropdown.current(0)
thread_dropdown_label = ttk.Label(root, text="Threads? ", font=("Calibri", 12))
thread_dropdown_label.place(relx=5/8, rely=1.5/9, width=width/8, height=height/9)

run_button = ttk.Button(root, text="Select a test to Run", command=click, bootstyle=SUCCESS)
run_button.place(relx=2/8, rely=5.5/9, width=width/2, height=2*height/9)

mainloop()
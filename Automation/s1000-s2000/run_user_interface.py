from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from test_controller import *

# called by the button. Starts running the tests based on options selected.
# will warn the user if they havent selected a system that they should have
def click():
    if type_var.get() == "":
        print("Select a system to test!")
    else:
        root.destroy()
        run_controller(type_var.get(), int(thread_count.get()), handle_repeats.get())
        check_protected_points(type_var.get())
        if type_var.get() == "S1000":
            get_radii_csv()
        kill_threads()

# called by the radio buttons to make the start button say the right thing based on which test its running
def change_button_text ():
    run_button.configure(text=f"Run Tests for {type_var.get()}")

# create a window and set its size, title, and prevent resizing
root = ttk.Window(themename="darkly")
width=750
height=500
root.geometry(f"{width}x{height}")
root.title ("LPSD Tester")
root.resizable(False, False)

# declare variables used by the components
type_var = StringVar()
thread_count = StringVar()
handle_repeats = StringVar()

# Create two radio buttons, one for system 1000 one for system 2000
for i in range(2):
    rb = ttk.Radiobutton(root, text=f"S{i+1}000", variable=type_var, value=f"S{i+1}000", bootstyle="light-outline toolbutton", command=change_button_text)
    rb.place(relx=1/8, rely=(1+i)/9 + 1/height, width= 2 * width/8, height=height/9 - 2)

# create combobox and label for thread count
thread_count_dropdown = ttk.Combobox(root, textvariable=thread_count, state=READONLY, bootstyle=LIGHT)
thread_count_dropdown['values'] = ('1','2','3','4')
thread_count_dropdown.place(relx=6/8, rely=1.25/9, width=width/8, height=30)
thread_count_dropdown.current(0)
thread_dropdown_label = ttk.Label(root, text="Threads? ", font=("Calibri", 12))
thread_dropdown_label.place(relx=5.06/8, rely=1/9, width=width/8 - 10, height=height/9)

# create combobox and label to handle duplicate tests
old_tests_dropdown = ttk.Combobox(root, textvariable=handle_repeats, state=READONLY, bootstyle=LIGHT)
old_tests_dropdown["values"] = ('rerun', 'skip')
old_tests_dropdown.place(relx=6/8, rely=2.25/9, width=width/8, height=30)
old_tests_dropdown.current(0)
old_tests_label = ttk.Label(root, text="Handle repeat tests?", font=("Calibri", 12))
old_tests_label.place(relx=4.25/8, rely=2/9, width=1.5*width/8, height=height/9)

# add the run button that calls click
run_button = ttk.Button(root, text="Select a test to Run", command=click, bootstyle=SUCCESS)
run_button.place(relx=2/8, rely=5.5/9, width=width/2, height=2*height/9)

mainloop()
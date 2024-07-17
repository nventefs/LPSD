import tkinter
import customtkinter

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import sys

sys.path.insert(0, 'C:/Users/E1176752/OneDrive - nVent Management Company/Documents/VSCode/Projects/LPSD/LPSD/')

from Multiplicative import multiplicative


import os
import subprocess
import time


def closemainloop():
    
    multi = []
    alphabet = []

    # EQUATION 1
    if(at_active.get()):
        multi.append(multiplicative.eq_h(float(at_Hf.get()) - float(at_H.get()), 0.175)) # EQ H
        alphabet.append("H")
    else:
        multi.append(multiplicative.eq_i(float(at_Hf.get()), 0.38)) # EQ I
        alphabet.append("I")

    # EQUATION 2
    if(at_isCorner.get()):
        multi.append(multiplicative.eq_t())
        alphabet.append("T")
    elif(at_isEdgeRectangular.get()):
        if(at_level0.get()):
            multi.append(multiplicative.eq_u(float(at_H0.get()), float(at_minwdith0.get()))) 
        if(at_extended.get()):
            multi.append(multiplicative.eq_u(float(at_H.get()), float(at_minwdith0.get())))
        else:
            multi.append(multiplicative.eq_u(float(at_H.get())-float(at_H0.get()), float(at_minwdith.get())))
        alphabet.append("U")
    elif(at_isFaceHorizontal.get()):
        if(at_level0.get()):
            H = float(at_H0.get())
            W = float(at_minwdith0.get())
        elif(at_extended.get()):
            H = float(at_H.get())
            W = float(at_minwdith0.get())
        else:
            H = float(at_H.get()) - float(at_H0.get())
            W = float(at_minwdith.get())
        multi.append(multiplicative.eq_v(H, W))
        alphabet.append("V")
    elif(at_isEdgeOval.get()):
        if(at_level0.get()):
            multi.append(multiplicative.eq_w(float(at_H0.get()), float(at_minwdith0.get()))) 
        elif(at_extended.get()):
            multi.append(multiplicative.eq_w(float(at_H.get()), float(at_minwdith0.get())))
        else:
            multi.append(multiplicative.eq_w(float(at_H.get())-float(at_H0.get()), float(at_minwdith.get())))
        alphabet.append("W")
    elif(at_isMiddleOval.get()):
        if(at_level0.get()):
            multi.append(multiplicative.eq_x(float(at_H0.get()), float(at_minwdith0.get()))) 
        elif(at_extended.get()):
            multi.append(multiplicative.eq_x(float(at_H.get()), float(at_minwdith0.get())))
        else:
            multi.append(multiplicative.eq_x(float(at_H.get())-float(at_H0.get()), float(at_minwdith.get())))
        alphabet.append("X")
    elif(at_isGableCorner.get()):
        if(at_level0.get()):
            multi.append(multiplicative.eq_y(float(at_H0.get()), float(at_minwdith0.get()))) 
            alphabet.append("Y")
        if(at_extended.get()):
            multi.append(multiplicative.eq_w(float(at_H.get()), float(at_minwdith0.get())))
            alphabet.append("W")
        else:
            multi.append(multiplicative.eq_w(float(at_H.get())-float(at_H0.get()), float(at_minwdith.get())))
            alphabet.append("W")
        multi.append(multiplicative.eq_y(float(at_H0.get()), float(at_minwdith0.get()))) 
        alphabet.append("Y")
    else:
        multi.append(multiplicative.eq_z(float(at_H0.get()), float(at_minwdith0.get())))
        alphabet.append("Z")

    # EQUATION 3
    if(at_level0.get() or at_extended.get()): # is level0 or extended
        multi.append(1)
        alphabet.append(" ")
    else:
        if(at_isCorner.get()):
            H = float(at_Hlvl.get()) - float(at_H0.get())
            W = float(at_minwdith.get())
            Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            multi.append(multiplicative.eq_j5(H, W, Hf))
            alphabet.append("J5") 
        elif(at_isEdgeRectangular.get()):
            H = float(at_Hlvl.get()) - float(at_H0.get())
            W = float(at_minwdith.get())
            Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            multi.append(multiplicative.eq_k5(H, W, Hf))
            alphabet.append("K5")
        elif(at_isFaceHorizontal.get()):
            multi.append(multiplicative.eq_l5(float(at_H.get()), float(at_H0.get()), float(at_minwdith.get()), float(at_Hf.get()))) 
            alphabet.append("L5")
        elif(at_isEdgeOval.get()):
            multi.append(multiplicative.eq_m5(float(at_H.get()) - float(at_H0.get()), float(at_minwdith.get()), float(at_Hf.get()) - float(at_Hlvl.get()))) 
            alphabet.append("M5")
        elif(at_isMiddleOval.get()):
            multi.append(multiplicative.eq_n5(float(at_Hlvl.get()) - float(at_H0.get()), float(at_minwdith.get()), float(at_Hf.get()) - float(at_Hlvl.get()))) 
            alphabet.append("N5")  
        elif(at_isGableCorner.get()):
            if(at_extended.get() or at_level0.get()):
                H = float(at_Hlvl.get())
            else:
                H = float(at_Hlvl.get()) - float(at_H0.get())
            multi.append(multiplicative.eq_o(H, float(at_minwdith.get()), float(at_Hf.get()), float(at_P.get()))) 
            alphabet.append("O")
        else:
            if(at_extended.get() or at_level0.get()):
                H = float(at_Hlvl.get())
            else:
                H = float(at_Hlvl.get()) - float(at_H0.get())
            multi.append(multiplicative.eq_p(H, float(at_minwdith.get()), float(at_Hf.get()), float(at_P.get()))) 
            alphabet.append("P")

    # EQUATION 4
    if(alphabet[-1] == " "):
        alphabet.append(" ")
        multi.append(1)
    else:
        multi.append(multiplicative.eq_s(float(at_Hlvl.get()))) 
        alphabet.append("S")
    
    # EQUATION 5
    if(at_level0.get() or at_extended.get()):
        if(at_isCorner.get()):
            if(at_level0.get()):
                H = float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_H0.get())
            elif(at_extended.get()):
                H = float(at_Hlvl.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            print("Formula J- H:{}, W:{}, Hf:{}".format(H, W, Hf))
            multi.append(multiplicative.eq_j(H,W,Hf))
            alphabet.append("J")
        elif(at_isEdgeRectangular.get()):
            if(at_level0.get()):
                H = float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_H0.get())
            elif(at_extended.get()):
                H = float(at_Hlvl.get())
                W = float(at_minwdith0.get())
                Hf = (float(at_Hf.get()) - float(at_Hlvl.get()))
            multi.append(multiplicative.eq_k(H,W,Hf)) 
            alphabet.append("K")
        elif(at_isFaceHorizontal.get()):
            H = float(at_H0.get())
            W = float(at_minwdith0.get())
            Hf = float(at_Hf.get()) - float(at_H0.get())
            multi.append(multiplicative.eq_l(H, W, Hf))
            alphabet.append("L")
        elif(at_isEdgeOval.get() or at_isMiddleOval.get()):
            if(at_level0.get()):
                H = float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_H0.get())
            elif(at_extended.get()):
                H = float(at_Hlvl.get()) - float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            else:
                H = float(at_Hlvl.get()) - float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            print("Formula M- H:{}, W:{}, Hf:{}".format(H, W, Hf))
            multi.append(multiplicative.eq_m(H,W,Hf)) 
            alphabet.append("M")
        elif(at_isGableCorner.get()):
            multi.append(multiplicative.eq_o()) #TODO: fill in values
            alphabet.append("O")
        else:
            multi.append(multiplicative.eq_p()) #TODO: fill in values
            alphabet.append("P")
    else:
        if(at_isCorner.get() or at_isEdgeRectangular.get() or at_isFaceHorizontal.get()):
            H = float(at_H0.get())
            W = float(at_minwdith0.get())
            Hf = float(at_Hf.get()) - float(at_H0.get())
            multi.append(multiplicative.eq_l(H, W, Hf))
            alphabet.append("L")
        elif(at_isEdgeOval.get() or at_isMiddleOval.get()):
            if(at_level0.get()):
                H = float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_H0.get())
            elif(at_extended.get()):
                H = float(at_Hlvl.get()) - float(at_H0.get())
                W = float(at_minwdith0.get())
                Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            else:
                H = float(at_Hlvl.get()) - float(at_H0.get())
                W = float(at_minwdith.get())
                Hf = float(at_Hf.get()) - float(at_Hlvl.get())
            print("Formula M- H:{}, W:{}, Hf:{}".format(H, W, Hf))
            multi.append(multiplicative.eq_m(H,W,Hf)) 
            alphabet.append("M")
        else:
            H = float(at_H0.get())
            W = float(at_minwdith0.get())
            Hf = float(at_Hf.get()) - float(at_H0.get())
            multi.append(multiplicative.eq_n(H, W, Hf))
            alphabet.append("N")


    print(multi)
    print(multi[0]*multi[1]*multi[2]*multi[3]*multi[4])
    print(alphabet)
    app.destroy()

#TODO: add JSON file optional selection to pull the following values:
# Minwidth lvl0, minwidth of lvl, lvl0 height, lvl height, ...

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("600x780")
app.title("Air Terminal Ki Engine")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, text="Air Terminal Multiplicative Calculation", justify=tkinter.LEFT)
label_1.pack(padx=10, pady=5)

at_active = customtkinter.CTkSwitch(master=frame_1, text = "Active")
at_active.pack(fill='both' , padx=10)

at_passive = customtkinter.CTkSwitch(master=frame_1, text = "Passive")
at_passive.pack(fill = 'both' , padx=10)

at_isCorner = customtkinter.CTkSwitch(master = frame_1, text = "isCorner")
at_isCorner.pack(fill = 'both', padx=10)

at_isEdgeRectangular = customtkinter.CTkSwitch(master = frame_1, text = "isEdgeRectangular")
at_isEdgeRectangular.pack(fill = 'both', padx=10)

at_isFaceHorizontal = customtkinter.CTkSwitch(master = frame_1, text = "isFaceHorizontal")
at_isFaceHorizontal.pack(fill = 'both', padx=10)

at_isEdgeOval = customtkinter.CTkSwitch(master = frame_1, text = "isEdgeOval")
at_isEdgeOval.pack(fill = 'both', padx=10)

at_isMiddleOval = customtkinter.CTkSwitch(master = frame_1, text = "isMiddleOval")
at_isMiddleOval.pack(fill = 'both', padx=10)

at_isGableCorner = customtkinter.CTkSwitch(master = frame_1, text = "isGableRidgeCorner or isGableEaveCorner")
at_isGableCorner.pack(fill = 'both', padx=10)

at_level0 = customtkinter.CTkSwitch(master = frame_1, text = "Level0")
at_level0.pack(fill = 'both', padx = 10, pady=5)

at_extended = customtkinter.CTkSwitch(master = frame_1, text = "Extended")
at_extended.pack(fill = 'both', padx = 10, pady=5)

label_2 = customtkinter.CTkLabel(master=frame_1, text="Level 0 Minimum Width (m)", justify=tkinter.LEFT)
label_2.pack(padx=10, pady=0)

at_minwdith0 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Level 0 Minimum Width", width = 400)
at_minwdith0.pack(pady=0, padx=10)

label_3 = customtkinter.CTkLabel(master=frame_1, text="Level 0 Height(m)", justify=tkinter.LEFT)
label_3.pack(padx=10, pady=0)

at_H0 = customtkinter.CTkEntry(master = frame_1, placeholder_text='Level 0 height', width = 400)
at_H0.pack(pady=0,padx=10)

label_4 = customtkinter.CTkLabel(master=frame_1, text="Level Height(m)", justify=tkinter.LEFT)
label_4.pack(padx=10, pady=0)

at_Hlvl = customtkinter.CTkEntry(master=frame_1, placeholder_text="Height (level)", width = 400)
at_Hlvl.pack(pady=0, padx=10)

label_5 = customtkinter.CTkLabel(master=frame_1, text="Level Minimum Width (m)", justify=tkinter.LEFT)
label_5.pack(padx=10, pady=0)

at_minwdith = customtkinter.CTkEntry(master=frame_1, placeholder_text="Level Minimum Width", width = 400)
at_minwdith.pack(pady=0, padx=10)

label_6 = customtkinter.CTkLabel(master=frame_1, text="Height at top of terminal (m)", justify=tkinter.LEFT)
label_6.pack(padx=10, pady=0)

at_Hf = customtkinter.CTkEntry(master=frame_1, placeholder_text="Height (top of air terminal)", width = 400)
at_Hf.pack(pady=0, padx=10)

label_7 = customtkinter.CTkLabel(master=frame_1, text="Heigth at base of terminal (m)", justify=tkinter.LEFT)
label_7.pack(padx=10, pady=0)

at_H = customtkinter.CTkEntry(master = frame_1, placeholder_text='Height (base)', width = 400)
at_H.pack(pady=0,padx=10)

label_8 = customtkinter.CTkLabel(master=frame_1, text="Pitch (m)", justify=tkinter.LEFT)
label_8.pack(padx=10, pady=0)

at_P = customtkinter.CTkEntry(master = frame_1, placeholder_text='Pitch (if applicable)', width = 400)
at_P.pack(pady=0,padx=10)

confirm = customtkinter.CTkButton(master = frame_1, text = "Calculate", command = closemainloop)
confirm.pack(fill = 'both', side = 'bottom')

app.mainloop()

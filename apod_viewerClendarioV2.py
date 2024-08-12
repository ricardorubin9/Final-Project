from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from PIL import ImageTk, Image, ImageColor
import tkinter as tk
import apod_desktop
import datetime
import os

# Initialize the image cache
apod_desktop.init_apod_cache()

# TODO: Create the GUI
root = Tk()
root.geometry('1000x700')

###### Inicio a insertar nuevo codigo
root.title("Astronomy Picture of the Day Viewer")
root.iconbitmap("nasa_logo_icon.ico")
image_bakground = ImageTk.PhotoImage(Image.open("NASA_logo.png").resize((300,300)))

# Create the frames
frm_input = ttk.Frame(root)
frm_input.grid(row=0, column=0, columnspan=2, pady=(20,10))

frm_images = ttk.Frame(root)
frm_images = ttk.LabelFrame(root, text="View Cached Image")
frm_images.grid(row=0, column=0, columnspan=2, pady=(10,20))

frm_more_images = ttk.Frame(root)
frm_more_images = ttk.LabelFrame(root, text="Get More Images")
frm_more_images.grid(row=0, column=3, columnspan=2, pady=(10,20), sticky=N)

frm_image_background = ttk.Frame(root)
frm_image_background.grid(row=7, column=1)

#TODO: Populate the user input frame with widgets
lbl_cached = ttk.Label (frm_images, text="Select Image:")
lbl_cached.grid(row=1, column=0, padx=(10,5), pady=5)

enter_cached = ttk.Entry(frm_images)
enter_cached.insert(0,"Select an image")
enter_cached.grid(row=1, column=1)

#Lo soguiente debe ser un boton
enter_desktop = ttk.Entry(frm_images)
enter_desktop.insert(0,"Set as Desktop")
enter_desktop.grid(row=1, column=2)

lbl_dates = ttk.Label (frm_more_images, text="Select Date(YYYY-mm-dd):")
lbl_dates.grid(row=1, column=3, padx=(10,5), pady=5)

date_pat= 'y-mm-dd'
v_today =datetime.datetime.now()
enter_dates = DateEntry(frm_more_images, maxdate=v_today, date_pattern=date_pat)

enter_dates.insert(0,"")
enter_dates.grid(row=1, column=4)
print (f"fecha seleccionada:{enter_dates.get()}")

#Lo soguiente debe ser un boton
enter_downloadI = ttk.Entry(frm_more_images)
enter_downloadI.insert(0,"Download Image")
enter_downloadI.grid(row=1, column=5)

lbl_image_backg = Label (frm_image_background, image=image_bakground)
lbl_image_backg.grid(row=7, column=1)

# Acciones para cada seleccion
##btn_get_info =ttk.Button(root, text="Download Image", command= terceroV3.get_apod_date)
##btn_get_info.grid(row=1, column=5)


###### Termino de insertar nuevo codigo
root.mainloop()
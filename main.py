import os
import requests
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime

app_id = os.environ["APP_ID"]
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'


def getweather(city_name):
    response = requests.get(url.format(city_name, app_id))
    if response:
        res = response.json()
        return res
    else:
        return print('Content not found!!!')


def weatherbycity():
    text1.delete('1.0', END)
    resp = getweather(search_city.get())
    if resp:
        temp = resp['main']
        degree = temp['temp']
        feels = temp['feels_like']
        a = resp['weather']
        status = a[0]['description']
        now = datetime.now()
        timestamp = now.strftime('%H:%M %p')
        char = f"\n\nCity: {search_city.get()}\nTemperature (Celsius): {degree}\nFeels like in (Celsius): {feels}\nDescription: {status}\nTime: {timestamp}"
        # When a PhotoImage object is garbage-collected by Python
        # (e.g. when you return from a function which stored an image in a local variable),
        # the image is cleared even if it’s being displayed by a Tkinter widget.
        # https://stackoverflow.com/a/27430839
        photo = ImageTk.PhotoImage(get_icon(resp))
        label = Label(image=photo)
        label.pack()
        label.img = photo
        text1.image_create('1.0', image=photo)
        text1.insert(END, chars=char)
    else:
        messagebox.showerror('City cannot found!!!' + search_city.get())


def get_icon(resp):
    mood = resp['weather']
    if mood[0]['main'] == 'Clouds':
        icon = Image.open("images/cloudy.png")
    elif mood[0]['main'] == 'Rain':
        icon = Image.open("images/rainy.png")
    elif mood[0]['main'] == 'Thunderstorm':
        icon = Image.open("images/storms.png")
    elif mood[0]['main'] == 'Snow':
        icon = Image.open("images/snow.png")
    elif mood[0]['main'] == 'Clear':
        icon = Image.open("images/sunny.png")
    else:
        icon = Image.open("images/default.png")
    return icon


# Create Gui for weather app
root = Tk()
root.title('Weather App')
root.geometry('700x600')

label1 = Label(root, text='City', font=('Arial', 18))
label1.pack(anchor="nw", padx=30, pady=15)

search_city = StringVar()
city = Entry(root, font=('Arial', 16), textvariable=search_city)
city.pack(anchor="nw", padx=30, pady=5)

button = Button(root, text='Show Current Weather', font=('Arial', 18), command=weatherbycity)
button.pack(anchor="nw", padx=30, pady=15)

notebook = ttk.Notebook(root)
notebook.pack(pady=15)

frame1 = ttk.Frame(notebook, width=500, height=130)
frame2 = ttk.Frame(notebook, width=500, height=130)

frame1.pack(fill='both', expand=True, pady=40)
frame2.pack(fill='both', expand=True, pady=40)

notebook.add(frame1, text='Current Weather')
notebook.add(frame2, text='Weekly Weather')

text1 = Text(frame1, width=300, height=150)
text1.pack()

text2 = Text(frame2, width=300, height=150)
text2.pack()

root.mainloop()


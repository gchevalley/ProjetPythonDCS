from Tkinter import *
import time



f = Tk()

default_entry_ticker = "ENTER Ticker"


def entry_ticker_event_enter(event):
    if str_entry_ticker.get() == default_entry_ticker:
        str_entry_ticker.set("")
        entry_ticker.config(fg="blue")

def entry_ticker_event_leave(event):
    if str_entry_ticker.get() == "":
        str_entry_ticker.set(default_entry_ticker)
        entry_ticker.config(fg="grey")
    

def update_clock():
    now = time.strftime("%H:%M:%S")
    print now
    label_time.configure(text=now)
    str_entry_ticker.set(default_entry_ticker)
    
    label_time.after(5000, update_clock)
    


now = time.strftime("%H:%M:%S")
label_time = Label(text=now)
label_time.pack()


str_entry_ticker = StringVar()
str_entry_ticker.set(default_entry_ticker)
entry_ticker = Entry(textvariable=str_entry_ticker)
entry_ticker.config(fg="grey")
entry_ticker.pack()
entry_ticker.bind('<Enter>', entry_ticker_event_enter)
entry_ticker.bind('<Leave>', entry_ticker_event_leave)

b1 = Button(text="hey")
b1.pack()

b1 = Button(text="hey")
b1.pack()

b1 = Button(text="hey")
b1.pack()

f.after(5000, update_clock)
f.mainloop()





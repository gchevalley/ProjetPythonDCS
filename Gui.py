from Tkinter import *
import utility
from Alert import *
import Monitor
from Ticker import *

import time


default_entry_ticker = "ENTER Ticker"

def entry_ticker_clear():
    str_entry_ticker.set(default_entry_ticker)
    entry_ticker.config(fg="grey")
    root.focus_set()

def entry_ticker_event_return(event):
    global block_refresh
    block_refresh = True
    tmp_ticker = Ticker(str_entry_ticker.get())
    
    if tmp_ticker.is_valid:
        str_label_last_price_value.set(str(tmp_ticker.last_price))
        
        msg = ''
        i = 0
        for tweet in tmp_ticker.relate_tweet:
            msg += tweet + "\n"
            i += 1
            
            if i == 5:
                break
        
        tweets_msg.set(msg)
        
    else:
        str_label_last_price_value.set("invalid symbol !")
    
    entry_ticker_clear()
    block_refresh = False     


def entry_ticker_event_enter(event):
    global block_refresh
    block_refresh = True
    if str_entry_ticker.get() == default_entry_ticker:
        str_entry_ticker.set("")
        entry_ticker.config(fg="blue")

def entry_ticker_event_leave(event):
    if str_entry_ticker.get() == "":
        entry_ticker_clear()
        global block_refresh
        block_refresh = False
    

def update_clock():
    if block_refresh == False:
        now = time.strftime("%H:%M:%S")
        print now
        label_time.configure(text=now)
        
    label_time.after(5000, update_clock) #recall
    

root = Tk()
root.title("Stocks monitor")

block_refresh = False
now = time.strftime("%H:%M:%S")
label_time = Label(text=now)
label_time.pack()


default_entry_ticker = "Enter Ticker"
str_entry_ticker = StringVar()
str_entry_ticker.set(default_entry_ticker)
entry_ticker = Entry(root,textvariable=str_entry_ticker)
entry_ticker.config(fg="grey")
entry_ticker.pack()
entry_ticker.bind('<Enter>', entry_ticker_event_enter)
entry_ticker.bind('<Leave>', entry_ticker_event_leave)
entry_ticker.bind('<Return>', entry_ticker_event_return)




str_label_last_price_value = StringVar()
str_label_last_price_value.set("#N/A")
label_last_price_value = Label(root, textvariable=str_label_last_price_value)
label_last_price_value.pack()


tweets_msg = StringVar()
tweets_msg.set("empty")
tweets = Message(root, textvariable=tweets_msg)
tweets.pack()


b1 = Button(root, text="Add to monitor")
b1.pack()

b2 = Button(root, text="Setup new alert")
b2.pack()


root.after(5000, update_clock)
root.mainloop()
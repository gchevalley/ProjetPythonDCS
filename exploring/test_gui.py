from Tkinter import *

def show_label():
    label.pack()

def hide_label():
    label.pack_forget()

f = Tk()
label = Label(text="Hello")
label.pack()
button1 = Button(text="Hide", command=hide_label)
button1.pack()
button2 = Button(text="Show", command=show_label)
button2.pack()


f.mainloop()
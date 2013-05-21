from Tkinter import *


root = Tk()

def read_data():
    for i in range(0, len(vec_data)):
        print vec_data[i].get()

vec_data = []

for i in range(0,3):
    str_entry = StringVar()
    tmp_label = Label(root, text=str(i))
    tmp_entry = Entry(root, textvariable=str_entry)
    
    vec_data.append(str_entry)
    
    tmp_label.grid(row=i, column=0)
    tmp_entry.grid(row=i, column=1)



tmp_button_read_data = Button(root, text='readdata', command=read_data)
tmp_button_read_data.grid(row=0, column=2)

root.mainloop()
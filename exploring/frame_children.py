from Tkinter import *

def btn_delete_selected_alerts():
    for item in f.winfo_children():
        print len(f.winfo_children())
        #print item.grid(row)
        #if  item['text'] == "6":
            #item.destroy()


root = Tk()

f = Frame(root)
f.grid(row=0, column=0)



for i in range(1,10):
    tmp_alert_cb_value = IntVar() # variable de type int (objet)
    tmp_alert_cb_value.set(0) # valeur initiale vaut 1
    tmp_alert_cb = Checkbutton(f, fg='red', text=str(i), variable=tmp_alert_cb_value)
    tmp_alert_cb.grid(row=0+i, column=0)
    #tmp_label_alert_ticker = Label(f, fg='red', text=str(i))
    #tmp_label_alert_ticker.grid(row=0+i, column=1, sticky='W')

btn_delete_alert_selected = Button(f, text="Delete selected", command=btn_delete_selected_alerts)
btn_delete_alert_selected.grid(row=0, column=3, sticky="E")

root.mainloop()
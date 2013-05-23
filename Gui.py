from Tkinter import *
from PIL import ImageTk, Image
import utility
from Alert import *
import Monitor
from Ticker import *
import thread

import time


default_entry_ticker = "ENTER Ticker"
refresh_time = 15 #en seconde pour les threads


def entry_ticker_clear():
    """vide l entry widget, met un texte par defaut en couleur gris"""
    str_entry_ticker.set(default_entry_ticker)
    entry_ticker.config(fg="grey")
    root.focus_set()


def entry_ticker_event_return(event):
    """event declenche lorsque la touche ENTER du clavier et frappee dans l entry widget"""
    load_ticker_data(str_entry_ticker.get())
    entry_ticker_clear()  


def entry_ticker_event_enter(event):
    """event declencher lorsque la souris passe au dessus ou rentre dans le widget entry"""
    if str_entry_ticker.get() == default_entry_ticker:
        str_entry_ticker.set("")
        entry_ticker.config(fg="blue")


def entry_ticker_event_leave(event):
    if str_entry_ticker.get() == "":
        entry_ticker_clear()
    

def update_clock():
    """fonction qui check regulierement quelles alertes sont actives"""
    
    while True:
        time.sleep(refresh_time)
        manage_alerts()
    

def load_ticker_data(symbol):
    """fonction qui va presenter les donnees financieres du produit financier desire"""
    if symbol != '':
        tmp_ticker = Ticker(symbol)
        
        if tmp_ticker.is_valid:
            str_label_symbol.set(header_symbol + tmp_ticker.symbol)
            str_label_last_price_value.set(header_last_price + str(tmp_ticker.last_price))
            daily_return = round(100*((tmp_ticker.last_price/tmp_ticker.previous_close)-1),2)
            str_label_return_1d_value.set(str(daily_return) + "%")
            
            if daily_return > 0:
                label_return_1d.config(fg="green")
                str_label_return_1d_value.set("+" + str_label_return_1d_value.get())
            else:
                label_return_1d.config(fg="red")
            
            str_label_company_name.set(header_company_name + tmp_ticker.company_name)
            
            
            
            msg = ''
            i = 0
            for tweet in tmp_ticker.relate_tweet:
                msg += tweet + "\n"
                i += 1
                
                if i == 5:
                    break
            
            tweets_msg.set(msg)
            
            
            if tmp_ticker.path_chart_1yr != '':
                img = ImageTk.PhotoImage(Image.open(tmp_ticker.path_chart_1yr))
                panel = Label(root, image = img)
                panel.image = img
                #panel.pack(side = "bottom", fill = "both", expand = "yes")
                panel.grid(row=6, columnspan=3, sticky="W")
            
        else:
            str_label_last_price_value.set("invalid symbol !")


def add_new_alert_from_window(widget_tl_to_close_if_successfull = None):
    """ajout d une alert dans la DB a partir de la pop-up fenetre"""
    #check requirements
    if str_label_alert_symbol.get() != '' and alert_action.get() != '' and str_entry_alert_limit.get() != '' and utility.is_number(str_entry_alert_limit.get()):
        
        tmp_ticker = Ticker(str_label_alert_symbol.get(), True)
        
        if tmp_ticker.is_valid:
            tmp_alert = Alert(tmp_ticker, alert_action.get(), float(str_entry_alert_limit.get()))
            
            widget_tl_to_close_if_successfull.destroy()
            thread.start_new_thread(manage_alerts, ())
    else:
        msgbox("Missing or incorrect required parameters !")


def btn_delete_selected_alerts():
    """suppression dans la DB des alerts selectionnees"""
    global warnings
    
    for i in range(0, len(vec_data_alerts)):
        if vec_data_alerts[i].get() == 1:
            warnings[i].removeAlertFromDb()
    
    #manage_alerts()
    thread.start_new_thread(manage_alerts, ())
    

def btn_setup_new_alert_open_alert_window():
    """fonction qui genere la pop window qui permet de creer de nouvelle alert"""
    tmp_symbol = str_label_symbol.get().replace(header_symbol, "")
    
    if tmp_symbol == '':
        tmp_symbol = str_entry_ticker.get().replace(default_entry_ticker, "")
    
    if tmp_symbol != '':
        
        tmp_symbol = tmp_symbol.upper()
        
        tl_alert = Toplevel()
        base_alert_title = "Set up new alert for " + tmp_symbol
        tl_alert.title(base_alert_title)
        
        label_alert_if = Label(tl_alert, text="if :")
        label_alert_if.grid(row=0, column=0)
        
        str_label_alert_symbol.set(tmp_symbol)
        label_alert_symbol = Label(tl_alert, textvariable=str_label_alert_symbol)
        label_alert_symbol.grid(row=1, column=0)
        
        alert_action.set("up")
        rb_alert_action_up = Radiobutton(tl_alert, text="Breaks UP", variable=alert_action, value="up")
        rb_alert_action_up.select()
        rb_alert_action_up.grid(row=1, column=1, sticky="W")
        rb_alert_action_down = Radiobutton(tl_alert, text="Breaks DOWN", variable=alert_action, value="down")
        rb_alert_action_down.grid(row=2, column=1, sticky="W")
        
        label_alert_limit = Label(tl_alert, text="Limit")
        label_alert_limit.grid(row=1, column=2)
        
        
        str_entry_alert_limit.set("")
        entry_alert_limit = Entry(tl_alert, textvariable=str_entry_alert_limit)
        entry_alert_limit.grid(row=2, column=2)
        
        btn_alert_add = Button(tl_alert, text ="Add", command=lambda: add_new_alert_from_window(tl_alert))
        btn_alert_add.grid(row=1, column=3)
        btn_alert_close = Button(tl_alert, text="Close window", command=tl_alert.destroy)
        btn_alert_close.grid(row=2, column=3)
        
    else:
        msgbox('no symbol')


def msgbox(msg):
    """fonction pour retourner des messages a l utilisateur sous forme de popup"""
    if msg != '':
        tl_msgbox = Toplevel()
        str_msgbox = StringVar()
        str_msgbox.set(msg)
        label_msgbox = Label(tl_msgbox, textvariable=str_msgbox)
        label_msgbox.pack()
        btn_msgbox_ok = Button(tl_msgbox, text="Ok", command=tl_msgbox.destroy)
        btn_msgbox_ok.pack()


def manage_alerts():
    """fonction qui affiche les alerts actives"""
    global warnings
    warnings = check_all_alert()
    
    start_row_alerts = 8

    #clean alerts area
    global frame_alert
    #frame_alert.grid_forget()
    frame_alert.destroy()
    frame_alert = Frame(root)
    frame_alert.grid(row=start_row_alerts, column=0)
    
    
    if len(warnings) > 0:
        
        #insere les nouvelles
        
        
        #delete les mortes
        
        
        
        global vec_data_alerts
        vec_data_alerts = []
    
        for i in range(0, len(warnings)): #receptionne un vec d objet
        
            tmp_alert_cb_value = IntVar() # variable de type int (objet)
            tmp_alert_cb_value.set(0) # valeur initiale vaut 1
            tmp_alert_cb = Checkbutton(frame_alert, text="", variable=tmp_alert_cb_value)
            tmp_alert_cb.grid(row=start_row_alerts+i, column=0)
            
            vec_data_alerts.append(tmp_alert_cb_value)
            
            tmp_label_alert_ticker = Label(frame_alert, fg='red', text=warnings[i].symbol + ' breaks ' + warnings[i].cross + ' ' + str(warnings[i].level))
            tmp_label_alert_ticker.grid(row=start_row_alerts+i, column=1, sticky='W')
        
        btn_delete_alert_selected = Button(frame_alert, text="Delete selected", command=btn_delete_selected_alerts)
        btn_delete_alert_selected.grid(row=start_row_alerts, column=3, sticky="E")
    
    else:
        
        tmp_label = Label(frame_alert, text="No alert")
        tmp_label.grid(row=start_row_alerts, column=0)




################################### GUI #####################################

root = Tk()
root.title("Stocks monitor")

block_refresh = False
now = time.strftime("%H:%M:%S")
label_time = Label(text=now)
#label_time.pack()



header_symbol = "Symbol: "
header_last_price = "Last price: "
#header_return_1d = "Intraday return: "
header_company_name = "Company: "


default_entry_ticker = "Enter Ticker"
str_entry_ticker = StringVar()
str_entry_ticker.set(default_entry_ticker)
entry_ticker = Entry(root, textvariable=str_entry_ticker)
entry_ticker.config(fg="grey")
entry_ticker.grid(row=0, columnspan=3, sticky='WE')
entry_ticker.bind('<Enter>', entry_ticker_event_enter)
entry_ticker.bind('<Button-1>', entry_ticker_event_enter)
entry_ticker.bind('<Leave>', entry_ticker_event_leave)
entry_ticker.bind('<Return>', entry_ticker_event_return)


str_label_symbol = StringVar()
str_label_symbol.set("")
label_symbol = Label(root, textvariable=str_label_symbol)
label_symbol.grid(row=1, column=0, sticky="W")

str_label_company_name = StringVar()
str_label_company_name.set("company: #N/A")
label_company_name = Label(root, textvariable=str_label_company_name)
label_company_name.grid(row=2, column=0, sticky="W")


str_label_last_price_value = StringVar()
str_label_last_price_value.set("Last price: #N/A")
label_last_price = Label(root, textvariable=str_label_last_price_value)
label_last_price.grid(row=3, column=0, sticky="W")


str_label_return_1d_value = StringVar()
str_label_return_1d_value.set("Intraday return: #N/A")
label_return_1d = Label(root, textvariable=str_label_return_1d_value)
label_return_1d.grid(row=3, column=1, sticky="W")



str_label_market_cap = StringVar()
str_label_market_cap.set("Market cap: #N/A")
label_market_cap = Label(root, textvariable=str_label_market_cap)
label_market_cap.grid(row=1, column=2, sticky="W")


str_label_pe = StringVar()
str_label_pe.set("P/E: #N/A")
label_pe = Label(root, textvariable=str_label_pe)
label_pe.grid(row=2,column=2, sticky="W")


str_label_eps = StringVar()
str_label_eps.set("EPS: #N/A")
label_eps = Label(root, textvariable=str_label_eps)
label_eps.grid(row=3, column=2, sticky="W")

str_label_beta = StringVar()
str_label_beta.set("Beta: #N/A")
label_beta = Label(root, textvariable=str_label_beta)
label_beta.grid(row=4, column=2, sticky="W")


str_date_nxt_ern = StringVar()
str_date_nxt_ern.set("Date next earnings: #N/A")
label_date_nxt_ern = Label(root, textvariable=str_date_nxt_ern)
label_date_nxt_ern.grid(row=5, column=2, sticky="W")




tweets_msg = StringVar()
tweets_msg.set("tweet empty")
tweets = Message(root, textvariable=tweets_msg)
tweets.grid(row=7, columnspan=4, sticky='W')



frame_alert = Frame(root)
frame_alert.grid(row=8, column=0)

label_no_alert = Label(frame_alert, text="no alert")
label_no_alert.grid(row=8, column=0)

warnings = []
vec_data_alerts = []
#manage_alerts()

b1 = Button(root, text="Add to monitor")
b1.grid(row=1, column=4)

b2 = Button(root, text="Setup new alert", command=btn_setup_new_alert_open_alert_window)
b2.grid(row=2, column=4)

b3 = Button(root, text="Show monitor")
b3.grid(row=3, column=4)


str_label_alert_symbol = StringVar()
alert_action = StringVar()
str_entry_alert_limit = StringVar()

thread.start_new_thread(update_clock, ())

root.mainloop()
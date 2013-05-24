from Tkinter import *
from PIL import ImageTk, Image
import utility
from Alert import *
from Monitor import *
from Ticker import *
import thread
import threading
import time
from random import randint


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
    if not utility.check_internet_connection():
        msgbox("Problem with the internet connection...")
        return False
        
    if symbol != '':
        tmp_ticker = Ticker(symbol)
        
        if tmp_ticker.is_valid:
            str_label_symbol.set(header_symbol + tmp_ticker.symbol)
            str_label_last_price_value.set(header_last_price + str(tmp_ticker.last_price))
            str_label_return_1d_value.set(str(tmp_ticker.daily_return) + "%")
            
            if tmp_ticker.daily_return > 0:
                label_return_1d.config(fg="green")
                str_label_return_1d_value.set("+" + str_label_return_1d_value.get())
            else:
                label_return_1d.config(fg="red")
            
            str_label_company_name.set(header_company_name + tmp_ticker.company_name)
            
            str_label_market_cap.set(header_market_cap + tmp_ticker.market_cap)
            
            str_label_pe.set(header_pe + str(tmp_ticker.pe))
            
            str_label_eps.set(header_eps + str(tmp_ticker.eps))
            
            str_label_beta.set(header_beta + str(tmp_ticker.beta))
            
            str_date_nxt_ern.set(header_date_nxt_ern + tmp_ticker.next_earnings_date)
            
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
                panel.grid(row=6, columnspan=3, sticky="W")
            
        else:
            str_label_last_price_value.set("invalid symbol !")


class UpdatePriceMonitor(threading.Thread):
    def __init__(self, data_to_update):
        threading.Thread.__init__(self)
        self.Terminated = False
        self.data_to_update = data_to_update
    def run(self):
        i = 0
        while not self.Terminated:
            time.sleep(refresh_time)
            for item in self.data_to_update:
                tmp_ticker = Ticker(item[1].symbol ,True)
                
                item[5].set(str(tmp_ticker.last_price))
                item[6].set(str(tmp_ticker.daily_return))
                
            
    def stop(self):
        self.Terminated = True


def kill_thread_refresh_price_monitor(tl_monitor, thread):
    thread.stop()
    tl_monitor.destroy()


def btn_monitor_delete_selected_idea():
    global vec_data_ideas
    
    for entry in vec_data_ideas:
        if entry[0].get() == 1:
            
            #del DB
            entry[1].deleteIdeaInDb()
            
            #del widget
            for i in range(2, 5):
                entry[i].destroy()
                
                
def btn_show_monitor():
    mon = Monitor()
    if len(mon.ideas) > 0:
        tl_monitor = Toplevel()
        th = thread.start_new_thread(manage_monitor, (mon, tl_monitor))
        #manage_monitor(mon, tl_monitor)
        
        
def manage_monitor(mon, tl_monitor):
    
    frame_monitor = Frame(tl_monitor)
    frame_monitor.grid(row=0, column=0)
    
    headers = ["Product", "Price", "Intraday return"]
    for i in range(0, len(headers)):
        tmp_label = Label(frame_monitor, text=headers[i])
        tmp_label.grid(row=0, column=i)
    
    btn_del_idea_selected = Button(frame_monitor, text="Delete selected", command=btn_monitor_delete_selected_idea)
    btn_del_idea_selected.grid(row=0, column=len(headers))
    
    global vec_data_ideas
    
    grid_row=1
    for idea in mon.ideas:
        tmp_ticker = Ticker(idea.symbol, True)
        if tmp_ticker.is_valid:
            
            tmp_idea_cb_value = IntVar() # variable de type int (objet)
            tmp_idea_cb_value.set(0) # valeur initiale vaut 1
            tmp_idea_cb = Checkbutton(frame_monitor, text=tmp_ticker.symbol, variable=tmp_idea_cb_value)
            tmp_idea_cb.grid(row=grid_row, column=0)
            
            str_label_last_price_value = StringVar()
            str_label_last_price_value.set(str(tmp_ticker.last_price))
            tmp_label_last_price = Label(frame_monitor, textvariable=str_label_last_price_value)
            tmp_label_last_price.grid(row=grid_row, column=1)
            
            str_label_intraday_return_value = StringVar()
            str_label_intraday_return_value.set(str(tmp_ticker.daily_return))
            tmp_label_intraday_return = Label(frame_monitor, textvariable=str_label_intraday_return_value)
            tmp_label_intraday_return.grid(row=grid_row, column=2)
            
            vec_data_ideas.append([tmp_idea_cb_value, idea, tmp_idea_cb, tmp_label_last_price, tmp_label_intraday_return, str_label_last_price_value, str_label_intraday_return_value])
            
            grid_row += 1
        
    
    #mise a jour des prix
    thread_update_price = UpdatePriceMonitor(vec_data_ideas)
    tl_monitor.protocol("WM_DELETE_WINDOW", lambda: kill_thread_refresh_price_monitor(tl_monitor, thread_update_price))
    thread_update_price.start()


def btn_setup_new_idea_to_monitor():
    
    if str_entry_ticker.get() != '' and str_entry_ticker.get() != default_entry_ticker:
        tmp_symbol = str_entry_ticker.get()
    else:
        tmp_symbol = str_label_symbol.get().replace(header_symbol, "")
    
    if tmp_symbol != '':
        idea = Idea(tmp_symbol)
        


def add_new_alert_from_window(widget_tl_to_close_if_successfull = None):
    """ajout d une alert dans la DB a partir de la pop-up fenetre"""
    #check requirements
    if str_label_alert_symbol.get() != '' and alert_action.get() != '' and str_entry_alert_limit.get() != '' and utility.is_number(str_entry_alert_limit.get()):
        
        tmp_ticker = Ticker(str_label_alert_symbol.get(), True)
        
        if tmp_ticker.is_valid:
            tmp_alert = Alert(tmp_ticker, alert_action.get(), float(str_entry_alert_limit.get()))
            
            widget_tl_to_close_if_successfull.destroy()

    else:
        msgbox("Missing or incorrect required parameters !")


def btn_delete_selected_alerts():
    """suppression dans la DB des alerts selectionnees, vecteur de vecteur a 2 dimension 0-> etat de la checkbox, 1->alert sous forme de text"""
    global warnings
    global frame_alert
    
    for i in range(0, len(vec_data_alerts)):
        if vec_data_alerts[i][0].get() == 1:
            warnings[i].removeAlertFromDb()
            
            #egalement detruire dans la frame
            for item in frame_alert.winfo_children():
                if item['text'] == vec_data_alerts[i][1]:
                    item.destroy()
    

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
    
    global frame_alert
    
    if len(warnings) > 0:
        
        global vec_data_alerts
        vec_data_alerts = []
        
        #ajouter uniquement les manquants
        for i in range(0, len(warnings)): #receptionne un vec d objet
            
            need_to_insert_alert = True
            for item in frame_alert.winfo_children():
                if item['text'] == str(warnings[i]):
                    need_to_insert_alert = False
                    break

            if need_to_insert_alert:
                
                tmp_alert_cb_value = IntVar() # variable de type int (objet)
                tmp_alert_cb_value.set(0) # valeur initiale vaut 1
                tmp_alert_cb = Checkbutton(frame_alert, text=str(warnings[i]), variable=tmp_alert_cb_value, fg='red')
                tmp_alert_cb.grid(row=start_row_alerts+len(frame_alert.winfo_children())-1, column=0, sticky='W')
                
                vec_data_alerts.append((tmp_alert_cb_value, str(warnings[i])))
        
        btn_delete_alert_selected = Button(frame_alert, text="Delete selected", command=btn_delete_selected_alerts)
        btn_delete_alert_selected.grid(row=start_row_alerts, column=3, sticky="E")
    
    else:
        
        tmp_label = Label(frame_alert, text="No alert")
        tmp_label.grid(row=start_row_alerts, column=0)



def btn_delete_selected_all_alerts():
    global vec_data_all_alerts
    
    for entry in vec_data_all_alerts:
        if entry[0].get() == 1:
            entry[1].removeAlertFromDb()
            entry[2].destroy()
    


def btn_show_all_alerts():
    global vec_data_all_alerts
    
    vec_all_alerts = get_all_alerts()
    
    k=0
    if len(vec_all_alerts) > 0:
        
        tl_all_alerts = Toplevel()
        frame_all_alerts = Frame(tl_all_alerts)
        frame_all_alerts.grid(row=0, column=0)
        
        for alert in vec_all_alerts:
            tmp_alert_cb_value = IntVar() # variable de type int (objet)
            tmp_alert_cb_value.set(0) # valeur initiale vaut 1
            tmp_alert_cb = Checkbutton(frame_all_alerts, text=str(alert), variable=tmp_alert_cb_value)
            tmp_alert_cb.grid(row=k, column=0, sticky='W')
            
            vec_data_all_alerts.append([tmp_alert_cb_value, alert, tmp_alert_cb])
            
            k += 1
        
        btn_all_alerts_delete_selected = Button(frame_all_alerts, text="Delete selected", command=btn_delete_selected_all_alerts)
        btn_all_alerts_delete_selected.grid(row=0, column=1)
    
    else:
        msgbox("no alert in DB !")
    


################################### GUI #####################################

root = Tk()
root.title("Stocks monitor")


header_symbol = "Symbol: "
header_last_price = "Last price: "
#header_return_1d = "Intraday return: "
header_company_name = "Company: "
header_market_cap = "Market Cap: "
header_pe = "P/E: "
header_eps = "EPS: "
header_beta = "Beta: "
header_date_nxt_ern = "Date next earnings: "


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
str_label_company_name.set("")
label_company_name = Label(root, textvariable=str_label_company_name)
label_company_name.grid(row=2, column=0, sticky="W")


str_label_last_price_value = StringVar()
str_label_last_price_value.set("")
label_last_price = Label(root, textvariable=str_label_last_price_value)
label_last_price.grid(row=3, column=0, sticky="W")


str_label_return_1d_value = StringVar()
str_label_return_1d_value.set("")
label_return_1d = Label(root, textvariable=str_label_return_1d_value)
label_return_1d.grid(row=3, column=1, sticky="W")


str_label_market_cap = StringVar()
str_label_market_cap.set("")
label_market_cap = Label(root, textvariable=str_label_market_cap)
label_market_cap.grid(row=1, column=2, sticky="W")


str_label_pe = StringVar()
str_label_pe.set("")
label_pe = Label(root, textvariable=str_label_pe)
label_pe.grid(row=2,column=2, sticky="W")


str_label_eps = StringVar()
str_label_eps.set("")
label_eps = Label(root, textvariable=str_label_eps)
label_eps.grid(row=3, column=2, sticky="W")


str_label_beta = StringVar()
str_label_beta.set("")
label_beta = Label(root, textvariable=str_label_beta)
label_beta.grid(row=4, column=2, sticky="W")


str_date_nxt_ern = StringVar()
str_date_nxt_ern.set("")
label_date_nxt_ern = Label(root, textvariable=str_date_nxt_ern)
label_date_nxt_ern.grid(row=5, column=2, sticky="W")


tweets_msg = StringVar()
tweets_msg.set("")
tweets = Message(root, textvariable=tweets_msg)
tweets.grid(row=7, columnspan=4, sticky='W')


frame_alert = Frame(root)
frame_alert.grid(row=8, column=0)

warnings = []
vec_data_alerts = []
vec_data_all_alerts = []
#manage_alerts()

vec_data_ideas = []



btn_show_monitor = Button(root, text="Show monitor", command=btn_show_monitor)
btn_show_monitor.grid(row=1, column=4)

btn_new_idea_for_monitor = Button(root, text="Add to monitor", command=btn_setup_new_idea_to_monitor)
btn_new_idea_for_monitor.grid(row=2, column=4)


btn_show_alerts = Button(root, text="Show all alerts", command=btn_show_all_alerts)
btn_show_alerts.grid(row=3, column=4)

btn_new_alert = Button(root, text="Setup new alert", command=btn_setup_new_alert_open_alert_window)
btn_new_alert.grid(row=4, column=4)




str_label_alert_symbol = StringVar()
alert_action = StringVar()
str_entry_alert_limit = StringVar()

thread.start_new_thread(update_clock, ())

root.mainloop()
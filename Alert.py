import Db
import Ticker

db = Db.Db()

class Alert():
    def __init__(self, ticker, cross, level, bypass_db = False):
        
        self.ticker = ticker
        self.symbol = ticker.symbol
        self.cross = cross
        self.level = level
        
        if bypass_db == False:
            #ajout dans db si n existe pas deja
            sql_query = "SELECT * FROM Alert WHERE symbol='" + ticker.symbol + "' AND cross='" + cross + "' AND level=" + str(level)
            extract_already_existing = db.select_query(sql_query)
            if len(extract_already_existing)>0:
                sql_query = "UPDATE ALERT SET price_last_refresh=" + str(ticker.last_price) + " WHERE symbol='" + ticker.symbol + "' AND cross='" + cross + "' AND level=" + str(level)
                db.exec_query(sql_query)
            else:
                self.insertAlertInDb(self.symbol, self.cross, self.level, ticker.last_price)
    
    def insertAlertInDb(self, symbol, cross, level, last_price = -1):
        db.insert_query('Alert', ((symbol, cross, level, last_price ),))
    
    def removeAlertFromDb(self):
        sql_query = "DELETE FROM Alert WHERE symbol='" + self.symbol + "' AND cross='" + self.cross + "' AND level=" + str(self.level)
        db.exec_query(sql_query)


def check_all_alert():
    
    warning = []
    
    all_alerts = db.get_table_content("Alert")
    for alert in all_alerts:
        ticker = Ticker.Ticker(alert[0])
        
        if ticker.is_valid and ticker.last_price > 0:
            if alert[1] == "up":
                if ticker.last_price > alert[2]:
                    tmp_alert = Alert(ticker, alert[1], alert[2], True)
                    warning.append(tmp_alert)
            elif alert[1] == 'down':
                if ticker.last_price < alert[2]:
                    tmp_alert = Alert(ticker, alert[1], alert[2], True)
                    warning.append(tmp_alert)
    
    return warning
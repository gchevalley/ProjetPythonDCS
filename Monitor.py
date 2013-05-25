import Db
import Ticker

db = Db.Db()

class Monitor():
    def __init__(self):
        self.ideas = []
        
        all_ideas = db.get_table_content("Monitor")
        
        for idea in all_ideas:
            self.ideas.append(Idea(idea[0], True))

class Idea():
    def __init__(self, symbol, bypass_add_to_db = False):
        
        self.symbol = symbol.upper()
        
        if not bypass_add_to_db:
            #ajout dans db si n existe pas deja
            sql_query = "SELECT * FROM Monitor WHERE symbol='" + self.symbol + "'"
            extract_already_existing = db.select_query(sql_query)
            
            if len(extract_already_existing)==0:
                self.insertIdeaInDb()
                
                
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    
    def insertIdeaInDb(self):
        """insere l alert dans la DB"""
        db.insert_query('Monitor', ((self.symbol,),))
    
    def deleteIdeaInDb(self):
        sql_query = "DELETE FROM Monitor WHERE symbol='" + self.symbol + "'"
        db.exec_query(sql_query)        
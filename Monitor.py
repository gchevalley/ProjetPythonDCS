import Db

class Monitor():
    def __init__(self):
        self.ideas = []
        
        db = Db.Db()
        all_ideas = db.get_table_content("Monitor")
        
        for idea in all_ideas:
            self.ideas.append(Idea(idea[0]))
        

class Idea():
    def __init__(self, ticker):
        self.ticker = ticker
        
        
mon = Monitor()
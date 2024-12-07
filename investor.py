class Investor:
    def __init__(self, name, num_investments, num_exits):
        self.name = name
        self.num_investments = num_investments
        self.num_exits = num_exits

    def calculate_score(self):
       
        return (self.num_investments * 1) + (self.num_exits * 2) # forumla = num_investments*1 + num_exits*2 

    def __str__(self):
        
        return f"Investor(name={self.name}, score={self.calculate_score()})"
    
    
# new column in datasets with score per investor - adjust code and have a new colunn added in a combined investor file 
#merge file
#dataset von investoren exportiert 



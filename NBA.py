
import xlrd
class team:
    """represents NBA team"""
    def __init__(self,name,div,conf):
        self.name = name
        self.div = div
        self.conf = conf
        self.record = (0,0,0)
    def __str__(self):
        return self.name + ", " + self.div + ", " + self.conf + "," + str(self.record)
        
class div:
    """represents NBA division"""
    def __init__(self,name,conf,team):
        self.name = name
        self.conf = conf
        self.teams={}
        self.add_team(team)
        
    def add_team(self,team):
        self.teams[team.name] = team
        
class conf: 
    """represents NBA conferences"""
    def __init__(self,name):
        self.name = name
        self.divs = {}

dict_conf = { "East": conf("East"), "West": conf("West")}
dict_teams = {}
#----------------------------------------------------------------------
def get_scores(path):
    """
    Open and read an scores file
    """
    book = xlrd.open_workbook(path)
    print ("--starting to parse scores--")
    div_data = book.sheet_by_index(1)
    day = 0
    for i in range(1230):
        row = div_data.row_values(i+1)
        if (day != row[0]):# if new day
            day = row[0]
            #check_elim()
        update_scores(row)
        
def get_teams(path):
    """
    Open and read an divisions file
    """
    book = xlrd.open_workbook(path)
    print ("--starting to parse divisions--")
    div_data = book.sheet_by_index(0)
    for i in range(30):
        
        row = div_data.row_values(i+1)
        curr_team = team(row[0],row[1], row[2])
        dict_teams[curr_team.name] = curr_team
        # create division if it doesn't exist
        curr_conf = dict_conf[row[2]]
        
        if (row[1] in curr_conf.divs ):
            curr_div = curr_conf.divs[row[1]]
            curr_div.add_team(curr_team)
        else:
            curr_div = div(row[1], row[2],curr_team)
            curr_conf.divs.update({row[1]:curr_div})
def update_scores(row):
    if ( row[4] = row[5]):
        print (row)
def status():
    for my_conf in dict_conf.values():
        print (my_conf.name)
        for my_div in my_conf.divs.values():
            print("   " + my_div.name)
            for my_team in my_div.teams.values():
                print ("       " + my_team.__str__())
                
#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "Analytics_Attachment.xlsx"
    get_teams(path)
    get_scores(path)
    status()
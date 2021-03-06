
verbose=False
import numpy as np 
import pandas as pd 
#Program for determining the playoff and elimination dates for teams

#Reads File
filename="Analytics_Attachment.xlsx"

divisions_table=pd.read_excel(filename, sheetname=0, header=0)
games=pd.read_excel(filename, sheetname=1, header=0)

East_div= divisions_table.loc[divisions_table.Conference_id=="East", :]
West_div= divisions_table.loc[divisions_table.Conference_id=="West", :] 
Conf_dict={"East":East_div,"West":West_div}

#Generates new columns
East_div.loc[:,"Wins"]=0 
East_div.loc[:,"Losses"]=0
East_div.loc[:,"Games Left"]=82
East_div.loc[:, "Eliminated"]=0
East_div.loc[:, "Playoffs"]=0
East_div.loc[:, "Date"]=""
East_div.loc[:, "Point Differential"]=0

West_div.loc[:,"Wins"]=0 
West_div.loc[:,"Losses"]=0
West_div.loc[:,"Games Left"]=82
West_div.loc[:,"Eliminated"]=0
West_div.loc[:, "Playoffs"]=0
West_div.loc[:, "Date"]=""
West_div.loc[:, "Point Differential"]=0


"""
def check_play(division, date):
	#Function to check if any teams have secure a playoff spot
	min_losses=division.iloc[7]["Losses"]
	min_wins=division.iloc[7]["Wins"]
	for index, row in division.iterrows():
		if row["Losses"]+row["Games Left"]==min_losses and row["Eliminated"]==0 and row["Playoffs"]==0:
			if tiebreaker(row["Team_Name"], division, min_wins, date):
				row["Playoffs"]=1
				row["Date"]=date
				division.loc[index]=row
		if row["Losses"]+row["Games Left"]<min_losses and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Playoffs"]=1
			row["Date"]=date
			division.loc[index]=row
	return division
"""
def add_points(team, points):
	#Adds point differential to get total point differential in a season
	conf=divisions_table[divisions_table.Team_Name==team]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_div.loc[East_div['Team_Name']==team, "Point Differential"]+=points
	elif conf=="West":
		West_div.loc[West_div['Team_Name']==team, "Point Differential"]+=points
	else:
		print("Uh Oh...")



def add_win(team):
	#function to add a win to winning team
	conf=divisions_table.loc[divisions_table.Team_Name==team, :]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_div.loc[East_div['Team_Name']==team, "Wins"]+=1
		East_div.loc[East_div['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_div.loc[West_div['Team_Name']==team, "Wins"]+=1
		West_div.loc[West_div['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")

def add_loss(team):
	#Function which adds a loss to a team
	conf=divisions_table.loc[divisions_table.Team_Name==team, :]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_div.loc[East_div['Team_Name']==team, "Losses"]+=1
		East_div.loc[East_div['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_div.loc[West_div['Team_Name']==team, "Losses"]+=1
		West_div.loc[West_div['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")

def check_elim(division, date):
	#Function to check if any teams have been eliminated because of games
	min_wins=division.iloc[7]["Wins"]
	for index, row in division.iterrows():
		if row["Wins"]+row["Games Left"]==min_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
			#hopefully this avoids a lot of the tiebreaking calculation...
			if not tiebreaker(row["Team_Name"], division, min_wins, date,0):
				row["Eliminated"]=1
				row["Date"]=date
				division.loc[index]=row
		elif row["Wins"]+row["Games Left"]<min_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Eliminated"]=1
			row["Date"]=date
			division.loc[index]=row
	return division


def head_to_head(team, other_team, division, date):
	#Function which returns 0 if team cannot win head to head vs other_team
	#Returns 1 if the team will win the head to head
	#Otherwise returns 2 for more tiebreaking
	team_wins=0
	other_wins=0
	games_left_between=0

	for index, row in games.iterrows():
		if row["Date"]<=date:
			if row["Home Team"]==team and row["Away Team"]==other_team:
				if row["Winner"]=="Home":
					team_wins+=1
				elif row["Winner"]=="Away":
					other_wins+=1
				else:
					print("Uh Oh...")
			elif row["Home Team"]==other_team and row["Away Team"]==team:
				if row["Winner"]=="Home":
					other_wins+=1
				elif row["Winner"]=="Away":
					team_wins+=1
				else: 
					print("Uh Oh...")
			else:
				pass
		else:
			if (row["Home Team"]==team and row["Away Team"]==other_team) or (row["Home Team"]==other_team and row["Away Team"]==team):
				games_left_between+=1

	if team_wins+games_left_between<other_wins:
		return 0
	elif team_wins+games_left_between>other_wins:
		return 1
	else:
		return 2

def divisionlead(team, other_team, team_div_name, other_div_name, division, date, is_div):
	#Function which returns 0 if team cannot win division tie breaker against other_team
	#Returns 1 if the team will win the divTieBreaker
	#Otherwise returns 2 for more tiebreaking
	team_lead=True
	other_lead=True

	team_div=division.loc[division["Division_id"]==team_div_name, :]
	other_div=division.loc[division["Division_id"]==other_div_name, :]

	team_div=team_div.sort_values(by="Wins", ascending=False)
	other_div=other_div.sort_values(by="Wins", ascending=False)

	team_div_max_wins=team_div.iloc[0]["Wins"]
	other_div_max_wins=other_div.iloc[0]["Wins"]

	if division.loc[division["Team_Name"]==team, "Wins"].values[0] + division.loc[division["Team_Name"]==team, "Games Left"].values[0] < team_div_max_wins:
		team_lead=False
	elif division.loc[division["Team_Name"]==team, "Wins"].values[0] + division.loc[division["Team_Name"]==team, "Games Left"].values[0] == team_div_max_wins:
		div_leader=team_div.loc[0, "Team_Name"].values[0]
		if (is_div ==0):
			if not (tiebreaker(team,division,wins,date, 1)):
				print ("divtie")
				team_lead=False
		#if head_to_head(team, div_leader, division, date)==0:###should actually recurse
		#	team_lead=False
	if division.loc[division["Team_Name"]==other_team, "Wins"].values[0] + division.loc[division["Team_Name"]==other_team, "Games Left"].values[0]<other_div_max_wins:
		other_lead=False
	elif division.loc[division["Team_Name"]==other_team, "Wins"].values[0] + division.loc[division["Team_Name"]==other_team, "Games Left"].values[0] == other_div_max_wins:
		other_leader=other_div.iloc[0]["Team_Name"]
		#if head_to_head(team, other_leader, division, date)==0:###should actually recurse but only one layer deep and not if other_leader = other team
		#	other_lead=False
		if (is_div ==0):
			if not (tiebreaker(other_team,division,wins,date, 1)):
				print ("divtie")
				other_lead=False
	if team_lead and not other_lead:
		return 1
	elif other_lead and not team_lead:
		return 0


def win_loss(team, other_team, teams, date):
	#Generates win loss record just within the inputted teams  
	team_names=teams.Team_Name.unique().tolist()
	teams.loc[:,"Wins"]=0
	teams.loc[:,"Losses"]=0
	teams.loc[:, "Games Left"]=0

	for index, row in games.iterrows():
		if row["Home Team"] == team or row["Away Team"] == other_team or row["Home Team"] == other_team or row["Away Team"] == team:
			if row["Date"]<	date:
				if row["Home Team"] in team_names and row["Away Team"] in team_names:
					if row["Winner"] =="Home":
						teams.loc[teams["Team_Name"]==row["Home Team"], "Wins"]+=1
					elif row["Winner"]=="Away":
						teams.loc[teams["Team_Name"]==row["Away Team"], "Wins"]+=1
			else:
				if row["Home Team"] in team_names and row["Away Team"] in team_names:
					if row["Home Team"] == team or row["Away Team"] == other_team:
						teams.loc[teams["Team_Name"]==row["Home Team"], "Wins"]+=1
					elif row["Away Team"] == team or row["Home Team"] == other_team:
						teams.loc[teams["Team_Name"]==row["Away Team"], "Wins"]+=1	
	print(teams if (verbose) else "")
	return teams
	
def div_record(team, other_team, teams, date):
	record = win_loss(team, other_team, teams, date)
	if record.loc[record["Team_Name"]==team, "Wins"].values[0] < record.loc[record["Team_Name"]==other_team, "Wins"].values[0]:
		print ("eliminated" + str(date) + team if (verbose) else "")
		return 0
	if record.loc[record["Team_Name"]==team, "Wins"].values[0] > record.loc[record["Team_Name"]==other_team, "Wins"].values[0]:
		print ("still possible" if (verbose) else "")
		return 1
	return 2
def conf_record(team, other_team, date):
	conf_name=divisions_table.loc[divisions_table["Team_Name"]==team, "Conference_id"].item()
	_conf_record = win_loss(team, other_team, Conf_dict[conf_name],date)

	if _conf_record.loc[_conf_record["Team_Name"]==team, "Wins"].values[0] < _conf_record.loc[_conf_record["Team_Name"]==other_team, "Wins"].values[0]:
		print ("eliminated" + str(date) + team if (verbose) else "")
		print (team + " vs " + other_team if (verbose) else "")
		print (our_conf_record if (verbose) else "")
		return 0
	if _conf_record.loc[_conf_record["Team_Name"]==team, "Wins"].values[0] > _conf_record.loc[_conf_record["Team_Name"]==other_team, "Wins"].values[0]:
		print ("still possible" if (verbose) else "")
		return 1
	return 2
def tiebreaker(team, division, wins, date, is_div):
	#Function to determine the outcome of tiebreakers
	#Returns False if a team is eliminiated (does not assert anything about making playoffs)

	#Find the number of teams in the tiebreak
	num_ties, dummy=division.loc[division["Wins"]==wins, :].shape

	if division.loc[division["Team_Name"]==team, "Games Left"].values[0] != 0:
		num_ties+=1

	if num_ties<2:
		return True

	#Two Team Tie Breaker
	elif num_ties==2:
		temp_div=division.loc[division["Team_Name"]!= team, :]
		other_team=temp_div.loc[temp_div["Wins"]==wins, "Team_Name"].values[0]

		#Head to Head Record
		head2head = head_to_head(team,other_team, division, date)
		if head2head==0:
			return False
		elif head2head==1:
			return True 
		#Division Leader... if a team can be division leader and other cannot return answer
		team_div_name=divisions_table.loc[divisions_table["Team_Name"]==team, "Division_id"].item()
		other_div_name=divisions_table.loc[divisions_table["Team_Name"]==other_team, "Division_id"].item()

		divlead=divisionlead(team, other_team, team_div_name, other_div_name, division, date, is_div)
		if (divlead ==0):
			return False
		if (divlead ==1):
			return True
			            
		#If teams are in same division, go by divison record
		#needs code
		if team_div_name==other_div_name:          
			teams=division.loc[division["Division_id"]==team_div_name, :]
			teams.append(division.loc[division["Team_Name"]==other_team, :])
			div_rec = div_record(team, other_team, teams, date)
			if (div_rec == 0):
				return False
			if (div_rec == 1):
				return True                     
		conf_rec = conf_record(team, other_team, date)
		if conf_rec == 0: 
			return False
		if conf_rec == 1:
			return True  
		print ("still tied: " + team + " with " + other_team + " " + str(date) )
		return True


	#Multi-team Tiebreaker
	#needs code
	else:
		temp_div=division.loc[division["Team_Name"]!= team, :]
		other_team=temp_div.loc[temp_div["Wins"]==wins, "Team_Name"]
		return True ### really should just rewrite head2head to be multiteam (and division leader)
		
        
for index, row in games.iterrows():
	date=row["Date"]
	if row["Winner"]=="Home":
		w=row["Home Team"]
		l=row["Away Team"]
		add_win(w)
		add_loss(l)
		add_points(w, row["Home Score"]-row["Away Score"])
		add_points(l, row["Away Score"]-row["Home Score"])
	elif row["Winner"]=="Away":
		w=row["Away Team"]
		l=row["Home Team"]
		add_win(w)
		add_loss(l)
		add_points(l, row["Home Score"]-row["Away Score"])
		add_points(w, row["Away Score"]-row["Home Score"])
	else:
		print("Uh Oh...")

	East_div=East_div.sort_values(by="Wins", ascending=False)
	West_div=West_div.sort_values(by="Wins", ascending=False)

	East_div=check_elim(East_div, date)
	West_div=check_elim(West_div, date)

total=East_div.append(West_div, ignore_index=True)

#total['Date']=pd.to_datetime(total['Date']).apply(lambda x: x.date())
total["Date"]=pd.to_datetime(total["Date"], errors="ignore", format="%m/%d/%Y")

total["Date"]=total["Date"].astype("str")


for index, row in total.iterrows():
	if row["Date"]=="":
		total.loc[index, "Date"]="Playoffs"
	else:
		replace=row["Date"].split(" ")[0]
		replace=replace.replace("-", "/")
		total.loc[index, "Date"]=replace

total=total.rename(columns={"Team_Name":"Team", "Date": "Date Eliminated"})

#Writes the results to an excel file
total.to_csv("Playoff_Results_ties.csv", columns=["Team", "Date Eliminated"], index=False)

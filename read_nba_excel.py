import numpy as np 
import pandas as pd 
#Program for determining the playoff and elimination dates for teams

#Reads File
filename="Analytics_Attachment.xlsx"

divisions_table=pd.read_excel(filename, sheetname=0, header=0)
games=pd.read_excel(filename, sheetname=1, header=0)

East_div= divisions_table.loc[divisions_table.Conference_id=="East", :]
West_div= divisions_table.loc[divisions_table.Conference_id=="West", :] 

#Generates new columns
East_div.loc[:,"Wins"]=0 
East_div.loc[:,"Losses"]=0
East_div.loc[:,"Games Left"]=82
East_div.loc[:, "Eliminated"]=0
East_div.loc[:, "Playoffs"]=0
East_div.loc[:, "Date"]=""
East_div.loc[:, "Total Points"]=0

West_div.loc[:,"Wins"]=0 
West_div.loc[:,"Losses"]=0
West_div.loc[:,"Games Left"]=82
West_div.loc[:,"Eliminated"]=0
West_div.loc[:, "Playoffs"]=0
West_div.loc[:, "Date"]=""
West_div.loc[:, "Total Points"]=0

def add_win(team):
	#function to add a win to winning team
	conf=divisions_table[divisions_table.Team_Name==team]
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
	conf=divisions_table[divisions_table.Team_Name==team]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_div.loc[East_div['Team_Name']==team, "Losses"]+=1
		East_div.loc[East_div['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_div.loc[West_div['Team_Name']==team, "Losses"]+=1
		West_div.loc[West_div['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")
def add_points(team, points):
	#Adds points to get total points in a season
	conf=divisions_table[divisions_table.Team_Name==team]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_div.loc[East_div['Team_Name']==team, "Total Points"]+=points
	elif conf=="West":
		West_div.loc[West_div['Team_Name']==team, "Total Points"]+=points
	else:
		print("Uh Oh...")

def check_elim(division, date):
	#Function to check if any teams have been eliminated because of games
	min_wins=division.iloc[7]["Wins"]
	for index, row in division.iterrows():
		if row["Wins"]+row["Games Left"]=min_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
			#hopefully this avoids a lot of the tiebreaking calculation...
			if not tiebreaker(row["Team_Name"], division, min_wins, date):
				row["Eliminated"]=1
				row["Date"]=date
				division.loc[index]=row
		elif row["Wins"]+row["Games Left"]<min_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Eliminated"]=1
			row["Date"]=date
			division.loc[index]=row
	return division

def check_play(division, date):
	#Function to check if any teams have secure a playoff spot
	min_losses=division.iloc[7]["Losses"]
	for index, row in division.iterrows():
		if row["Losses"]+row["Games Left"]<min_losses and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Playoffs"]=1
			row["Date"]=date
			division.loc[index]=row
	return division

def tiebreaker(team, division, wins, date):
	#Function to determine the outcome of tiebreakers
	#Returns False if a team is eliminiated (does not assert anything about making playoffs)

	#Find the number of teams in the tiebreak
	num_ties, dummy=division.loc[division["Wins"]==wins, :].shape
	if division.loc[division["Team_Name"]==team, "Games Left"] != 0:
		num_ties+=1

	if num_ties<2: 
		return True

	#Two Team Tie Breaker
	elif num_ties==2:
		other_team=division.loc[division["Wins"]==wins, "Team_Name"]

		#Head to Head Record
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
			return False
		elif other_wins+games_left_between<team_wins:
			return True
		else:
			#Division Leader... if a team can be division leader and other cannot return answer
			team_lead=True
			other_lead=True



			if team_lead and not other_lead:
				return True
			elif other_lead and not team_lead:
				return False
			else:
				#If teams are in same division, go by divison record



		

	#Multi-team Tiebreaker
	else:




for index, row in games.iterrows():
	date=row["Date"]
	if row["Winner"]=="Home":
		w=row["Home Team"]
		l=row["Away Team"]
		add_win(w)
		add_loss(l)
		add_points(w, row["Home Score"])
		add_points(l, row["Away Score"])
	elif row["Winner"]=="Away":
		w=row["Away Team"]
		l=row["Home Team"]
		add_win(w)
		add_loss(l)
		add_points(l, row["Home Score"])
		add_points(w, row["Away Score"])
	else:
		print("Uh Oh...")

	East_div=East_div.sort_values(by="Wins", ascending=False)
	West_div=West_div.sort_values(by="Wins", ascending=False)

	East_div=check_elim(East_div, date)
	West_div=check_elim(West_div, date)

	East_div=check_play(East_div, date)
	West_div=check_play(West_div, date)

#Writes the results to an excel file
writer=pd.ExcelWriter("Playoff_Results_tie.xlsx", engine="xlsxwriter", date_format="mm/dd/yyyy", datetime_format="mm/dd/yyyy")
East_div.to_excel(writer, sheet_name="East")
West_div.to_excel(writer, sheet_name="West")
writer.save()

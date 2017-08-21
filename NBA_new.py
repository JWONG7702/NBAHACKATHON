import numpy as np 
import pandas as pd 


#Reads File
filename="Analytics_Attachment.xlsx"

teams=pd.read_excel(filename, sheetname=0, header=0)
games=pd.read_excel(filename, sheetname=1, header=0)

East_conf= teams.loc[teams.Conference_id=="East", :]
West_conf= teams.loc[teams.Conference_id=="West", :] 

#Generate New Columns
East_conf.loc[:,"Wins"]=0 
East_conf.loc[:,"Losses"]=0
East_conf.loc[:,"Games Left"]=82
East_conf.loc[:, "Eliminated"]=0
East_conf.loc[:, "Playoffs"]=0
East_conf.loc[:, "Date"]=""

West_conf.loc[:,"Wins"]=0 
West_conf.loc[:,"Losses"]=0
West_conf.loc[:,"Games Left"]=82
West_conf.loc[:,"Eliminated"]=0
West_conf.loc[:, "Playoffs"]=0
West_conf.loc[:, "Date"]=""

def add_win(team):
	#Function which adds a win to a team
	conf=teams.loc[teams.Team_Name==team, :]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_conf.loc[East_conf['Team_Name']==team, "Wins"]+=1
		East_conf.loc[East_conf['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_conf.loc[West_conf['Team_Name']==team, "Wins"]+=1
		West_conf.loc[West_conf['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")

def add_loss(team):
	#Function which adds a loss to a team
	conf=teams.loc[teams.Team_Name==team, :]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_conf.loc[East_conf['Team_Name']==team, "Losses"]+=1
		East_conf.loc[East_conf['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_conf.loc[West_conf['Team_Name']==team, "Losses"]+=1
		West_conf.loc[West_conf['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")

def write_excel(filename):
	#writes the East and West Conferences to an excel file 
	writer=pd.ExcelWriter(filename, engine="xlsxwriter", date_format="mm/dd/yyyy", datetime_format="mm/dd/yyyy")
	East_conf.to_excel(writer, sheet_name="East")
	West_conf.to_excel(writer, sheet_name="West")
	writer.save()

def check(conference, date):
	#checks for sure if a team is eliminated (guaranteed)
	eighth_wins=conference.iloc[7]["Wins"]
	for index, row in conference.iterrows():
		if row["Wins"]+row["Games Left"]< eighth_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Eliminated"]=1
			row["Date"]=date
			conference.loc[index, :]=row
	return conference

def assign_results(team, games_left, win):
	#assigns win/loses to a team returns assigned games if complete but 0 if an error. 
	if win==True:
		for index, row in games_left.iterrows():
			if row["Home Team"]==team and row["Winner"]=="":
				games_left.loc[index, "Winner"]="Home"
			elif row["Home Team"]==team and row["Winner"]=="Away":
				return (games_left, False)
			elif row["Away Team"]==team and row["Winner"]=="":
				games_left.loc[index, "Winner"]="Away"
			elif row["Away Team"]==team and row["Winner"]=="Home":
				return (games_left, False)
			else:
				pass
		return (games_left, True)

	elif win==False:
		for index, row in games_left.iterrows():
			if row["Home Team"]==team and row["Winner"]=="":
				games_left.loc[index, "Winner"]="Away"
			elif row["Home Team"]==team and row["Winner"]=="Home":
				return (games_left, False)
			elif row["Away Team"]==team and row["Winner"]=="":
				games_left.loc[index, "Winner"]="Away"
			elif row["Away Team"]==team and row["Winner"]=="Away":
				return (games_left, False)
			else:
				pass
		return (games_left, True)

def try_elim(team, conference, date):
	#Function which tries to get the team to not be eliminated
	#Returns True if team can be in playoffs and False if not
	games_before=games.loc[games["Date"]<=date, :]
	games_after=games.loc[games["Date"]>date, :]

	#tries to assign victories to all remaining games
	games_after.loc[:, "Winner"]=""
	breaker=True

	while breaker:
		#assigns all wins to team
		games_after, breaker=assign_results(team, games_after, True)

		#assigns loses to all tied for 8th place teams
		eighth_wins=conference.iloc[7]["Wins"]
		eighth_teams=conference[conference["Wins"]==eighth_wins, :]
		num_eighth_teams, dummy= eighth_teams.shape
		for i in range(0, num_eighth_teams):
			other_team=eighth_teams.iloc[i]["Team_Name"]
			games_after, breaker= assign_results(team, games_after, False)

		rank()
		if in playoffs return true


	return breaker

def random_assign(games_after):
	#randomly assigns victories to the remaining teams
def rank(team, conference):
	#ranks the teams in the conference at the end


#Main Function
date=""
for index, row in games.iterrows():
	#Only recalculates eliminations at the end of every day
	if row["Date"] != date:
		East_conf=East_conf.sort_values(by="Wins", ascending=False)
		West_conf=West_conf.sort_values(by="Wins", ascending=False)
		East_conf=check(East_conf, date) 
		West_conf=check(West_conf, date)
		date=row["Date"]

	if row["Winner"]=="Home":
		w=row["Home Team"]
		l=row["Away Team"]
	elif row["Winner"]=="Away":
		w=row["Away Team"]
		l=row["Home Team"]
	else:
		print("Uh Oh...")

	add_win(w)
	add_loss(l)

write_excel("Playoff_Results_new.xlsx")

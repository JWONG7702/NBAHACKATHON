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
	eighth_loses=conference.iloc[7]["Losses"]

	for index, row in conference.iterrows():
		if row["Wins"]+row["Games Left"]< eighth_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Eliminated"]=1
			row["Date"]=date
			conference.loc[index, :]=row
		elif row["Losses"] + row["Games Left"]< eighth_loses and row["Eliminated"]==0 and row["Playoffs"]==0:
			row["Playoffs"]=1
			row["Date"]=date
			conference.loc[index, :]=row
	return conference

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


#Tries to update the guaranteed dates

def add_win_hyp(team):
	#Function which adds a win to a team
	conf=teams.loc[teams.Team_Name==team, :]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_hyp.loc[East_hyp['Team_Name']==team, "Wins"]+=1
		East_hyp.loc[East_hyp['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_hyp.loc[West_hyp['Team_Name']==team, "Wins"]+=1
		West_hyp.loc[West_hyp['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")

def add_loss_hyp(team):
	#Function which adds a loss to a team
	conf=teams.loc[teams.Team_Name==team, :]
	conf=conf.iloc[0]["Conference_id"]
	if conf=="East":
		East_hyp.loc[East_hyp['Team_Name']==team, "Losses"]+=1
		East_hyp.loc[East_hyp['Team_Name']==team, "Games Left"]-=1
	elif conf=="West":
		West_hyp.loc[West_hyp['Team_Name']==team, "Losses"]+=1
		West_hyp.loc[West_hyp['Team_Name']==team, "Games Left"]-=1
	else:
		print("Uh Oh...")

def gen_conference(date):
	#generates the conference standings at the end of a certain date (then update for hypotheticals)
	East_hyp= teams.loc[teams.Conference_id=="East", :]
	West_hyp= teams.loc[teams.Conference_id=="West", :] 

	#Generate New Columns
	East_hyp.loc[:,"Wins"]=0 
	East_hyp.loc[:,"Losses"]=0
	East_hyp.loc[:,"Games Left"]=82
	East_hyp.loc[:, "Eliminated"]=0
	East_hyp.loc[:, "Playoffs"]=0
	East_hyp.loc[:, "Date"]=""

	West_hyp.loc[:,"Wins"]=0 
	West_hyp.loc[:,"Losses"]=0
	West_hyp.loc[:,"Games Left"]=82
	West_hyp.loc[:,"Eliminated"]=0
	West_hyp.loc[:, "Playoffs"]=0
	West_hyp.loc[:, "Date"]=""

	for index, row in games.iterrows():
		if row["Date"]<=date:
				if row["Winner"]=="Home":
					w=row["Home Team"]
					l=row["Away Team"]
				elif row["Winner"]=="Away":
					w=row["Away Team"]
					l=row["Home Team"]
				else:
					print("Uh Oh...")

		add_win_hyp(w)
		add_loss_hyp(l)
	return East_hyp, West_hyp

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
		#teams with higher wins than our team should win all their games if possible
		#teams which cannot make playoffs should also win all possible games

	return breaker

def random_assign(games_after):
	#randomly assigns victories to the remaining teams
	return True
def h2h(team, other_team, date):
	#Head to Head record for two teams
	#Returns 0 if unsolved, 1 if team loses and 2 if team wins
	for index, row in games.iterrows():
		team_wins=0
		other_wins=0
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
	if team_wins==other_wins:
		return 0
	elif team_wins<other_wins:
		return 1
	elif team_wins>other_wins:
		return 2

def win_loss(teams, date):
	#Generates win loss record just within the inputted teams
	team_names=teams.Team_Name.unique().tolist()
	teams.loc[:,"Wins"]=0
	teams.loc[:,"Losses"]=0

	for index, rows in games.iterrows():
		if row["Date"]<date:
			if row["Home Team"] in team_names and row["Away Team"] in team_names:
				if row["Winner"]=="Home":
					teams.loc[teams["Team_Name"]==row["Home Team"], "Wins"]+=1
					teams.loc[teams["Team_Name"]==row["Away Team"], "Losses"]+=1
				elif row["Winner"]=="Away":
					teams.loc[teams["Team_Name"]==row["Home Team"], "Losses"]+=1
					teams.loc[teams["Team_Name"]==row["Away Team"], "Wins"]+=1

	for index, row in teams.iterrows():
		teams.iloc[index]["Win Rate"]=teams.iloc[index]["Wins"]/(teams.iloc[index]["Wins"]+teams.iloc[index]["Losses"])
	teams.sort_values(by="Win Rate", ascending=False)	
	return teams

def is_div_leader(team, conference, date):
	#Function which returns True is the team is the current division leader and False if not
	team_div=conference.loc[conference["Team_Name"]==team, "Division_id"]
	division=conference.loc[conference["Division_id"]==team_div, :]

	division.loc[:, "Div_Tiebreak"]=0
	division=division.sort_values(by=["Wins", "Tiebreak"], asceding=[False, False])

	div_leader_wins=division.iloc[0]["Wins"]
	a, b= division.loc[division["Wins"]==div_leader_wins, :].shape
	if division.loc[division["Team_Name"]==team, "Wins"]!=div_leader_wins:
		return False
	elif a==1:
		return True
	elif a==2:
		temp=division.loc[division["Team_Name"]!=team, :]
		div_other_team=temp.loc[temp["Wins"]==div_leader_wins, "Team_Name"]
		h2h_result=h2h(team, div_other_team, date)
		if h2h_result==1:
			return False
		elif h2h_result==2:
			return True
		else: 
			#division win loss
			division_in=win_loss(division, date)
			if division_in.loc[division_in["Team_Name"]==team, "Win Rate"]>division_in.loc[division_in["Team_Name"]==div_other_team, "Win Rate"]:
				return True
			elif division_in.loc[division_in["Team_Name"]==team, "Win Rate"]<division_in.loc[division_in["Team_Name"]==div_other_team, "Win Rate"]:
				return False
			else:
				#conference win rates
				for index, rows in conference.iterrows():
					conference.iloc[index]["Win Rate"]=conference.iloc[index]["Wins"]/(conference.iloc[index]["Wins"]+conference.iloc[index]["Losses"])
				conference=conference.sort_values(by="Win Rate", ascending=False)
				if conference.loc[conference["Team_Name"]==team, "Win Rate"] > conference.loc[conference["Team_Name"]==div_other_team, "Win Rate"]:
					return True
				elif conference.loc[conference["Team_Name"]==team, "Win Rate"] < conference.loc[conference["Team_Name"]==div_other_team, "Win Rate"]:
					return False
				else:
					print(team_div + "still has a tie")
					return False
	else:
		multi_div_in=win_loss(division.loc[division["Wins"]==div_leader_wins, :], date)
		multi_div_teams=multi_div_in.Team_Name.unique().tolist()
		if mutli_div_in.loc[multi_div_in["Team_Name"]==team, "Win Rate"] == multi_div_in.iloc[0]["Win Rate"]: 
			if multi_div_in.iloc[0]["Win Rate"] != multi_div_in.iloc[1]["Win Rate"]:
				return True
			else: 
				#skips division win-loss
				#conference win loss
				for index, rows in conference.iterrows():
					conference.iloc[index]["Win Rate"]=conference.iloc[index]["Wins"]/(conference.iloc[index]["Wins"]+conference.iloc[index]["Losses"])
				conference=conference.sort_values(by="Win Rate", ascending=False)
				if conference.loc[conference["Team_Name"]==team, "Win Rate"] == conference.iloc[0]["Win Rate"]:
					if conference.iloc[0]["Win Rate"] != conference.iloc[1]["Win Rate"]:
						return True
					else: 
						print(team_div + "still has a tie")
						return False
				else:
					return False
		else: 
			return False

def rank(conference, date):
	#ranks the teams in the conference based on tiebreak rules (based on games already played)
	conference.loc[:, "Tiebreak"]=0
	conference=conference.sort_values(by=["Wins", "Tiebreak"], ascending=[False, False])
	for index, row in conference.iterrows():
		team=row["Team_Name"]
		wins=row["Wins"]
		ties, dummy=conference.loc[conference["Wins"]==wins, :].shape
		if ties==1:
			pass
		elif ties==2 and row["Tiebreak"]==0:
			#two way tiebreaker
			#returns 1 if the team loses the tiebreak and 2 if the team wins
			two_way(team, wins, row, conference, date)
			temp=conference.loc[conference["Team_Name"]!=team, :]
			other_team=temp.loc[temp["Wins"]==wins, "Team_Name"]
			row["Tiebreak"]=h2h(team, other_team, date) #Head to Head Record
			if row["Tiebreak"]==0:
				#Division Leader
				if is_div_leader(team, conference, date) and not is_div_leader(other_team, conference, date):
					row["Tiebreak"]==2
				elif not is_div_leader(team, conference, date) and is_div_leader(other_team, conference, date):
					row["Tiebreak"]==1
				else:
					team_div=conference.loc[conference["Team_Name"]==team, "Division_id"]
					other_team_div=conference.loc[conference["Team_Name"]==other_team, "Division_id"]
					if team_div==other_team_div:
						#division record
						division=conference.loc[conference["Division_id"]==team_div, :]
						division_in=win_loss(division, date)
						if division_in.loc[division_in["Team_Name"]==team, "Win Rate"]>division_in.loc[division_in["Team_Name"]==other_team, "Win Rate"]:
							row["Tiebreak"]=2
						elif division_in.loc[division_in["Team_Name"]==team, "Win Rate"]<division_in.loc[division_in["Team_Name"]==other_team, "Win Rate"]:
							row["Tiebreak"]=1
						else:
							#conference record
							for index, rows in conference.iterrows():
								conference.iloc[index]["Win Rate"]=conference.iloc[index]["Wins"]/(conference.iloc[index]["Wins"]+conference.iloc[index]["Losses"])
							if conference.loc[conference["Team_Name"]==team, "Win Rate"] > conference.loc[conference["Team_Name"]==other_team, "Win Rate"]:
								row["Tiebreak"]=2
							elif conference.loc[conference["Team_Name"]==team, "Win Rate"] < conference.loc[conference["Team_Name"]==other_team, "Win Rate"]:
								row["Tiebreak"]=1
							else:
								print(team + "and" + other_team + "still has a tie")

		elif row["Tiebreak"]==0:
			#Multi-way tiebreaker
			tied_teams=conference.loc[conference["Wins"]==wins, :]
			tied_team_names=conference.loc[conference["Wins"]==wins, "Team_Name"].unique().tolist()

			#Checks if these teams are division leaders
			for i in tied_team_names:
				if is_div_leader(i, conference, date):
					conference.loc[conference["Team_Name"]==i, "Tiebreak"]=1
				#checks for changes...			
		conference.loc[index, :]=row

	conference=conference.sort_values(by=["Wins", "Tiebreak"], ascending=[False, False])
	return conference


#second main function



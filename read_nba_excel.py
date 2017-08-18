import numpy as np 
import pandas as pd 
#Program for determining the playoff and elimination dates for teams

#Reads File
filename="Analytics_Attachment.xlsx"

divisions_table=pd.read_excel(filename, sheetname=0, header=0)
games=pd.read_excel(filename, sheetname=1, header=0)

East_div= divisions_table[divisions_table.Conference_id=="East"]
West_div= divisions_table[divisions_table.Conference_id=="West"] 

#Generates new columns
East_div.loc[:,"Wins"]=0 
East_div.loc[:,"Losses"]=0
East_div.loc[:,"Games Left"]=82
East_div.loc[:, "Eliminated"]=0
East_div.loc[:, "Playoffs"]=0
East_div.loc[:, "Date"]=""

West_div.loc[:,"Wins"]=0 
West_div.loc[:,"Losses"]=0
West_div.loc[:,"Games Left"]=82
West_div.loc[:,"Eliminated"]=0
West_div.loc[:, "Playoffs"]=0
West_div.loc[:, "Date"]=""

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

def check_elim(division, date):
	#Function to check if any teams have been eliminated because of games
	min_wins=division.iloc[7]["Wins"]
	for index, row in division.iterrows():
		if row["Wins"]+row["Games Left"]<min_wins and row["Eliminated"]==0 and row["Playoffs"]==0:
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


for index, row in games.iterrows():
	date=row["Date"].split(" ")[0]
	if row["Winner"]=="Home":
		w=row["Home Team"]
		l=row["Away Team"]
		add_win(w)
		add_loss(l)
	elif row["Winner"]=="Away":
		w=row["Away Team"]
		l=row["Home Team"]
		add_win(w)
		add_loss(l)
	else:
		print("Uh Oh...")

	East_div=East_div.sort_values(by="Wins", ascending=False)
	West_div=West_div.sort_values(by="Wins", ascending=False)

	East_div=check_elim(East_div, date)
	West_div=check_elim(West_div, date)

	East_div=check_play(East_div, date)
	West_div=check_play(West_div, date)
		
print(East_div)
print(West_div)







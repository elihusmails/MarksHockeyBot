#!/usr/bin/env python

import requests
import json
import arrow

#
# Copied from https://github.com/dword4/hockeystats/blob/master/hockeystats.py
# Modified to work with my bot
#

def teamStats(command):
    """ Gets team stats including games played, wins, losses ot. usage: !nhl_teamstats WSH """
    teamName = command.split()
    try:
        if teamName is not None:
            teamId = getTeamId(teamName[1])
            msg = getTeamStats(teamId)
        else:
            msg = "please search using 3 letter team abbreviation"
    except:
        return "unable to find team id"
    return msg
    
def pGame(command):
    """ Gets last game information for a team. usage: !nhl_lastgame TOR """
    teamName = command.split()
    try:
        if teamName is not None:
            teamId = getTeamId(teamName[1])
            msg = prevGame(teamId)
        else:
            msg = "please search using 3 letter team abbreviation"
    except:
        return "unable to find team id"
    return msg

def nGame(command):
    """ Gets next game information for a team. usage: !nhl_nextgame MTL """
    teamName = command.split()
    try:
        if teamName is not None:
            teamId = getTeamId(teamName[1])
            msg = nextGame(teamId)
        else:
            msg = "please search using 3 letter team abbreviation"
    except:
        return "unable to find team id"
    return msg

def divisionStandings(division):
    """ Grab standings for a division: Options: Metro(politan), Atlantic, Central, Pacific. usage: !nhl_division <full division name> """
    getStandings()
    try:
        if division is not None:
            divId = getDivisionId(division)
            getStandings()
            msg = getDivisionStandings(divId)
        else:
            msg = "Options: Metro(politan), Atlantic, Central, Pacific"
    except:
        msg = "Options: Metro(politan), Atlantic, Central, Pacific"
    return msg

def currentGameScores():
    """ Gets the scores of all games scheduled to start today """
    return getCurrentGameScores()

def getAbbrToFullname(teamName):
	""" Get the full name of a 3 letter abbreviation. usage: !nhl_abbreviation WPG """ 
	try:
		fullName = abbrToFullname(teamName)
		if fullName is False:
			msg = "failure to chooch: specify a correct 3 letter abbreviation"
		else:
			msg = "%s = %s" % (teamName.upper(), fullName)
		return msg
	except:
		return "failure to chooch"

# team stats (gp, win, loss, ot)
def getTeamStats(teamid):
    req = "https://statsapi.web.nhl.com/api/v1/teams/"+str(teamid)+"/stats"
    r = requests.get(req)
    
    team_stats_json = r.text
    team_stats = json.loads(team_stats_json)
    
    teamName = team_stats['stats'][0]['splits'][0]['team']['name']
    gamesPlayed = team_stats['stats'][0]['splits'][0]['stat']['gamesPlayed']
    wins = team_stats['stats'][0]['splits'][0]['stat']['wins']
    losses = team_stats['stats'][0]['splits'][0]['stat']['losses']
    ot = team_stats['stats'][0]['splits'][0]['stat']['ot']
    pts = team_stats['stats'][0]['splits'][0]['stat']['pts']

    teamStats = "%s GP %s (%s-%s-%s) %s PTS" % (teamName, gamesPlayed, wins, losses, ot, pts)
    return teamStats

# prev game details
def prevGame(teamid):
    req = "https://statsapi.web.nhl.com/api/v1/teams/"+str(teamid)+"?expand=team.schedule.previous"
    r2 = requests.get(req)

    game_last_json = r2.text
    game_last = json.loads(game_last_json)
    date = game_last['teams'][0]['previousGameSchedule']['dates'][0]['date']
    home_team = game_last['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']
    away_team = game_last['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']

    prevGameDetails = date + " | " +away_team['team']['name'] + " @ " +home_team['team']['name'] + " | " + str(away_team['score']) + " - " + str(home_team['score']) + " Final"
    return prevGameDetails

# next game detail
def nextGame(teamid):
    req = "https://statsapi.web.nhl.com/api/v1/teams/"+str(teamid)+"?expand=team.schedule.next"
    r2 = requests.get(req)

    game_last_json = r2.text
    game_last = json.loads(game_last_json)
    date = game_last['teams'][0]['nextGameSchedule']['dates'][0]['date']
    home_team = game_last['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']
    away_team = game_last['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']
    game_data = game_last['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate']
    a = arrow.get(game_data)
    nextGameDetails = date + " | " +away_team['team']['name'] + " @ " +home_team['team']['name'] + " at " +str(a.to('US/Eastern').time()) + " EST"
    return nextGameDetails

# get the division id
def getDivision(teamid):
    req = "https://statsapi.web.nhl.com/api/v1/teams/"+str(teamid)
    r = requests.get(req)
    team_info_json = r.text
    team_info = json.loads(team_info_json)
    return(team_info['teams'][0]['division']['id'])

# get team abbreviation from ID
def getTeamAbbr(ID):
    teams = {
            "NJD" : 1,
            "NYI" : 2,
            "NYR" : 3,
            "PHI" : 4,
            "PIT" : 5,
            "BOS" : 6,
            "BUF" : 7,
            "MTL" : 8,
            "OTT" : 9,
            "TOR" : 10,
            "CAR" : 12,
            "FLA" : 13,
            "TBL" : 14,
            "WSH" : 15,
            "CHI" : 16,
            "DET" : 17,
            "NSH" : 18,
            "STL" : 19,
            "CGY" : 20,
            "COL" : 21,
            "EDM" : 22,
            "VAN" : 23,
            "ANA" : 24,
            "DAL" : 25,
            "LAK" : 26,
            "SJS" : 28,
            "CBJ" : 29,
            "MIN" : 30,
            "WPG" : 52,
            "ARI" : 53,
            "VGK" : 54
            }
    for team, teamId in teams.items():
        if teamId == ID:
            ret = team
    return ret

# get team ID from abbreviation
def getTeamId(abbreviation):
    teams = {
            "NJD" : 1,
            "NYI" : 2,
            "NYR" : 3,
            "PHI" : 4,
            "PIT" : 5,
            "BOS" : 6, 
            "BUF" : 7,
            "MTL" : 8,
            "OTT" : 9,
            "TOR" : 10,
            "CAR" : 12,
            "FLA" : 13,
            "TBL" : 14,
            "WSH" : 15,
            "CHI" : 16,
            "DET" : 17,
            "NSH" : 18,
            "STL" : 19,
            "CGY" : 20,
            "COL" : 21,
            "EDM" : 22,
            "VAN" : 23,
            "ANA" : 24,
            "DAL" : 25,
            "LAK" : 26,
            "SJS" : 28,
            "CBJ" : 29,
            "MIN" : 30,
            "WPG" : 52,
            "ARI" : 53,
            "VGK" : 54
            }
    team = abbreviation.upper()

    if team in teams:
        return teams[team.upper()] 
    else:
        return False

# convert 3 letter abbreviations to full names
def abbrToFullname(abbr):
    teams = {
            "NJD" : "New Jersey Devils",
            "NYI" : "New York Islanders",
            "NYR" : "New York Rangers",
            "PHI" : "Philadelphia Flyers",
            "PIT" : "Pittsburgh Penguins",
            "BOS" : "Boston Bruins",
            "BUF" : "Buffalo Sabres",
            "MTL" : "Montreal Canadiens",
            "OTT" : "Ottowa Senators",
            "TOR" : "Toronto Maple Leafs",
            "CAR" : "Carolina Hurricanes",
            "FLA" : "Florida Panthers",
            "TBL" : "Tampa Bay Lightning",
            "WSH" : "Washington Capitals",
            "CHI" : "Chicago Blackhawks",
            "DET" : "Detroit Red Wings",
            "NSH" : "Nashville Predators",
            "STL" : "St. Louis Blues",
            "CGY" : "Calgary Flames",
            "COL" : "Colorado Avalanche",
            "EDM" : "Edmonton Oilers",
            "VAN" : "Vancouver Canucks",
            "ANA" : "Anaheim Ducks",
            "DAL" : "Dallas Stars",
            "LAK" : "Los Angeles Kings",
            "SJS" : "San Jose Sharkes",
            "CBJ" : "Columbus Blue Jackets",
            "MIN" : "Minnesota Wild",
            "WPG" : "Winnipeg Jets",
            "ARI" : "Arizona Coyotes",
            "VGK" : "Vegas Golden Knights"
            }
    if abbr.upper() in teams.keys():
        return teams[abbr.upper()]
    else:
        return False

# get division id value
def getDivisionId(division):
    divisions = {
            "ATLANTIC" : 17,
            "CENTRAL" : 16,
            "METROPOLITAN" : 18,
            "METRO" : 18,
            "PACIFIC" : 15
            }
    if division.upper() in divisions:
        return divisions[division.upper()]
    else:
        return False

# get league wide standings
def getStandings():
    req = "http://statsapi.web.nhl.com/api/v1/standings"
    r = requests.get(req)
    standings_info_json = r.text
    standings_info = json.loads(standings_info_json)
    #print(standings_info['records'][0]['division']['id'])
    #print(standings_info['records'][0]['division']['name'])
    global divisionData
    divisionData = {}
    for n in standings_info['records']:
        divisionId = n['division']['id']
        i = 1
        division_blob = ''
        for nn in range(0,3):
            pts = n['teamRecords'][nn]['points']
            team_name = n['teamRecords'][nn]['team']['name'] 
            division_blob += "%s (%s) %s pts" % (team_name, i, pts)
            if i == 3:
                pass
            else: 
                division_blob += ", "
            i += 1
        divisionData[divisionId] = division_blob

def getDivisionStandings(did):
    # getStandings() needs to be called to make sure data is fresh
    return divisionData[did] 

# get the scores of today's games
def getCurrentGameScores():
    req = "https://statsapi.web.nhl.com/api/v1/schedule"
    r = requests.get(req)
    ret = ''

    game_list_json = r.text
    game_list = json.loads(game_list_json)

    i = 0
    limit = len(game_list['dates'][0]['games']) - 1
    for game in game_list['dates'][0]['games']:
        gameStatus = game['status']['abstractGameState']
        if gameStatus == 'Live':
            team_away_id = game['teams']['away']['team']['id']
            team_home_id = game['teams']['home']['team']['id']
            team_away_name = game['teams']['away']['team']['name']
            team_home_name = game['teams']['home']['team']['name']
            team_away_score = game['teams']['away']['score']
            team_home_score = game['teams']['home']['score']
            team_away_abbr = getTeamAbbr(team_away_id)
            team_home_abbr = getTeamAbbr(team_home_id)
            ret = ret + "live: \x02%s\x02@\x02%s\x02 %s-%s\n" % (team_away_abbr, team_home_abbr, team_away_score, team_home_score)
        elif gameStatus == 'Final':
            team_away_name = game['teams']['away']['team']['name']
            team_home_name = game['teams']['home']['team']['name']
            team_away_id = game['teams']['away']['team']['id']
            team_home_id = game['teams']['home']['team']['id']
            team_away_score = game['teams']['away']['score']
            team_home_score = game['teams']['home']['score']
            team_away_abbr = getTeamAbbr(team_away_id)
            team_home_abbr = getTeamAbbr(team_home_id)
            ret = ret + "final: \x02%s\x02@\x02%s\x02 %s-%s Final\n" % (team_away_abbr, team_home_abbr, team_away_score, team_home_score)
        else:
            game_state = game['status']['detailedState']
            game_time = game['gameDate']
            team_away_name = game['teams']['away']['team']['name']
            team_home_name = game['teams']['home']['team']['name']
            team_away_id = game['teams']['away']['team']['id']
            team_home_id = game['teams']['home']['team']['id']
            team_away_score = game['teams']['away']['score']
            team_home_score = game['teams']['home']['score']
            team_away_abbr = getTeamAbbr(team_away_id)
            team_home_abbr = getTeamAbbr(team_home_id)
            a_game_time = arrow.get(game_time)
            game_time_local = a_game_time.to('US/Eastern').format('HHmm')
            ret = ret + "Not Started: \x02%s\x02@\x02%s\x02 at %s EST\n" % (team_away_abbr, team_home_abbr, game_time_local)
        # if i == 0:
        #     ret += msg
        #     ret += " / "
        # elif i == limit:
        #     ret += msg
        # else:
        #     ret += msg
        #     ret += " / "
        # i += 1
    return ret

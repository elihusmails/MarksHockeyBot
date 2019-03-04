import json
import urllib.request
import datetime
from collections import OrderedDict
from operator import itemgetter

class Brains():

    #
    # Utility Functions
    #

    def downloadJson( self, theUrl ):
        response = urllib.request.urlopen(theUrl)
        data = response.read()
        text = data.decode('utf-8')
        jsonData = json.loads( text )
        return jsonData

    def getTodaysDate(self):
      x = datetime.datetime.now()
      return x.strftime("%Y-%m-%d")  

    #
    # End Utility Functions
    # 

    def processHelp(self):
        return """
            Mark's Hockey Bot (c) 2019

            Supported Commands:
            $hello - Say hello to the bot
            $status - Provide bot status
            $games - lists today\'s games
            $scores - lists today\'s scores
            $standings - lists current standings
            $standings.expanded - lists expanded standings
            $scoring.top - lists top 10 scoring leaders
            $scores - lists the scores of today\'s games
            $team.stats [3 digit team name]= Team stats
            $team.prev [3 digit team name] - Score from teams previous game
            $team.next [3 digit team name] - When is teams next game
        """

    def getStatus(self):
        return """
            I\'m good
        """

    def getTopScorers(self):
        link = 'http://www.nhl.com/stats/rest/skaters?isAggregate=true&reportType=basic&isGame=false&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameTypeId=2%20and%20seasonId%3E=20182019%20and%20seasonId%3C=20182019'

        response = 'P\tG\tA\tPlayer\n'
        jsonResponse = self.downloadJson(link)
        count = 0
        for p in jsonResponse['data']:
            # response = response + p['points'] + '\t' + p['goals'] + '\t' + p['assists'] + '\t' + p['playerName'] 
            response = response + "{}\t{}\t{}\t{}\n".format(p['points'], p['goals'], p['assists'], p['playerName'])
            count += 1
            if count > 10:
                break

        return response

    def getStandings(self):
        link = 'http://www.nhl.com/stats/rest/team?isAggregate=false&reportType=basic&isGame=false&reportName=franchisesummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22wins%22,%22direction%22:%22DESC%22}]&cayenneExp=gameTypeId=2%20and%20seasonId%3E=20182019%20and%20seasonId%3C=20182019'

        response = 'Points\tTeam\n'
        jsonResponse = self.downloadJson(link)
        for t in jsonResponse['data']:
            response = response + "{}\t\t{}\n".format(t['points'], t['franchisePlaceName'])

        return response


    def getTodaysGames(self):
        link = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}&hydrate=team'.format(self.getTodaysDate(), self.getTodaysDate())
        jsonResponse = self.downloadJson(link)

        response = ''

        index = 0
        for game in jsonResponse['dates'][0]['games']:

            # gameLink = 'https://statsapi.web.nhl.com/' + game['link']
            # gameJsonResponse = self.downloadJson(gameLink)

            homeTeam = game['teams']['home']['team']['abbreviation']
            awayTeam = game['teams']['away']['team']['abbreviation']

            response = response + "{}\t{}\n".format(homeTeam, awayTeam)

        return response

    def getTodaysScores(self):
        link = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}&hydrate=team()'.format(self.getTodaysDate(), self.getTodaysDate())
        jsonResponse = self.downloadJson(link)

        response = ''

        index = 0
        for game in jsonResponse['dates'][0]['games']:

            # gameLink = 'https://statsapi.web.nhl.com/' + game['link']
            # gameJsonResponse = self.downloadJson(gameLink)

            homeTeam = game['teams']['home']['team']['abbreviation']
            awayTeam = game['teams']['away']['team']['abbreviation']

            homeTeamScore = game['teams']['home']['score']
            awayTeamScore = game['teams']['home']['score']

            response = response + "{} {}\t{} {}\n".format(homeTeam, homeTeamScore, awayTeam, awayTeamScore)

        return response

    def getTeamStats(self, command):

        stat = command.split()

        link = 'https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats'
        jsonResponse = self.downloadJson(link)

        statMap = {}

        for team in jsonResponse['teams']:
            teamStats = team['teamStats'][0]['splits'][0]['stat']
            theStat = teamStats[stat[1]]
            statMap.update({team['abbreviation']:theStat})

        msg = ''
        d = OrderedDict(sorted(statMap.items(), key=itemgetter(1), reverse=True))

        for key,value in d.items():
            msg = msg + "{}\t{}\n".format(key, str(value))

        return msg

    def getSupportedTeamStats(self):
        link = 'https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats'
        jsonResponse = self.downloadJson(link)

        msg = ''
        teamStats = jsonResponse['teams'][0]['teamStats'][0]['splits'][0]['stat']
        for stat in teamStats:
            msg = msg + stat + '\n'

        return msg

    def getTeamStatRanking(self, command):
        team = command.split()

        link = 'https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats'
        jsonResponse = self.downloadJson(link)

        statMap = {}

        msg = ''
        for t in jsonResponse['teams']:
            if t['abbreviation'] == team[1]:
                teamStats = t['teamStats'][0]['splits'][1]['stat']
                for stat in teamStats:
                    msg = msg + "{}\t{}\n".format(stat, teamStats[stat])

        return msg

    def getExpandedStandings(self):
        link = 'https://statsapi.web.nhl.com/api/v1/standings?expand=standings.record'
        jsonResponse = self.downloadJson(link)

        msg = "\t{}\t{}\t{}\t{}\t{}\t{}\n".format( 
            'team'.ljust(20),
            'wins'.ljust(3),
            'losses'.ljust(3),
            'ot'.ljust(3),
            'points'.ljust(3),
            'streak'.ljust(3))

        records = jsonResponse['records']
        for record in records:
            msg = "{}{} / {}\n".format(msg, record['conference']['name'], record['division']['nameShort'])
            for team in record['teamRecords']:
                msg = "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(msg, 
                    team['team']['name'].ljust(20),
                    str(team['leagueRecord']['wins']).ljust(3),
                    str(team['leagueRecord']['losses']).ljust(3),
                    str(team['leagueRecord']['ot']).ljust(3),
                    str(team['points']).ljust(3),
                    str(team['streak']['streakCode'].ljust(3)))

        return msg

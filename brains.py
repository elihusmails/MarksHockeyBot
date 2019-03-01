import json
import urllib.request
import datetime

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
            $top scorers - lists top 10 scoring leaders
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
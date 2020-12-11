from schedule import *
import schedule
import time

print("Importing....")

from twitt import *
from GetDatas import *

print("import done!")


class match:
    Id = ""
    Dom = ""
    DomTag = ""
    Away = ""
    AwayTag = ""
    Tag = ""
    ScorerDom = ""
    ScorerAway = ""
    RedCardDom = ""
    RedCardAway = ""
    LineupHome = ""
    LineupAway = ""
    Status = ""
    Hour = ""

    def __init__(self, id):
        self.Id = id
        self.Dom, self.Away, self.Hour = getMatchsInfos(id)
        self.DomTag = getTag(self.Dom)
        self.AwayTag = getTag(self.Away)
        self.Tag = "#" + self.DomTag + self.AwayTag
        self.ScorerDom, self.ScorerAway, self.RedCardDom, self.RedCardAway = getMatchUpdate(self.Id)
        self.LineupHome = ""
        self.LineupAway = ""
        self.Status = getMatchStatus(self.Id)
        schedule.every().day.at(timeop(self.Hour, 0, -30, 0)).do(self.getLU).tag(self.Tag)
        self.PrepareForMatch()

    def PrepareForMatch(self):
        schedule.every(30).seconds.do(self.actualisation).tag(self.Tag)

    def score(self):
        return str(len(self.ScorerDom)) + "-" + str(len(self.ScorerAway))

    def actualisation(self):
        stat = self.Status
        if stat == "FMT" or stat == "SMT":
            self.match_update()
            self.time_update()
        else:
            self.time_update()
            self.match_update()

    def time_update(self):
        stat = getMatchStatus(self.Id)
        if self.Status != stat:
            self.Status = stat
            if stat == "Match Finished":
                TweetFin(self.Dom, self.Away, self.Tag, self.score())
                schedule.clear(self.Tag)

    def match_update(self):
        ScorD, ScorA, RCD, RCA = getMatchUpdate(self.Id)
        if len(ScorD) != len(self.ScorerDom):
            NS = ScorD[len(self.ScorerDom):]
            for s in NS:
                self.ScorerDom.append(s)
                TweetGoal(self.DomTag, s[1], s[0], self.Tag, self.score())
        if len(ScorA) != len(self.ScorerAway):
            NS = ScorA[len(self.ScorerAway):]
            for s in NS:
                self.ScorerAway.append(s)
                TweetGoal(self.AwayTag, s[1], s[0], self.Tag, self.score())
        if len(RCD) != len(self.RedCardDom):
            NS = RCD[len(self.RedCardDom):]
            for s in NS:
                self.RedCardDom.append(s)
                TweetRedCard(self.DomTag, s[1], s[0], self.Tag, self.score())
        if len(RCA) != len(self.RedCardAway):
            NS = RCA[len(self.RedCardAway):]
            for s in NS:
                self.RedCardAway.append(s)
                TweetRedCard(self.AwayTag, s[1], s[0], self.Tag, self.score())

    def getLU(self):
        return ""


def timeop(t, htoadd, mtoadd, stoadd):
    hour = int(t[0:2]) + htoadd
    min = int(t[3:5]) + mtoadd
    while min < 0:
        min += 60
        hour -= 1
    while min > 60:
        min -= 60
        hour += 1
    sec = int(t[6:8]) + stoadd
    while sec < 0:
        sec += 60
        min -= 1
    while sec > 60:
        sec -= 60
        min += 1
    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
    if min < 10:
        min = "0" + str(min)
    else:
        min = str(min)
    if sec < 10:
        sec = "0" + str(sec)
    else:
        sec = str(sec)
    ret = str(hour) + ":" + str(min) + ":" + str(sec)
    return ret


def getTag(team):
    D = {
        "Lyon": "OL",
        "Stade de Reims": "SDR",
        "Ajax": "AJAX",
        "Atalanta": "ATAL",
        "FC Midtjylland": "FCM",
        "Liverpool": "LIV",
        "Bayern Munich": "FCB",
        "Lok. Moscow": "LOK",
        "SV Salzburg": "SVS",
        "Ath Madrid": "ATH",
        "Real Madrid": "MAD",
        "Mönchengladbach": "MOCH",
        "Inter": "INTER",
        "Shakhtar Donetsk": "SHD",
        "Man City": "CITY",
        "Marseille": "OM",
        "Olympiakos": "OLYM",
        "FC Porto": "FCP",
        "Paris SG": "PSG",
        "Istanbul Basaksehir": "BAS",
        "St Etienne": "ASSE",
        "Angers": "SCO"
    }
    return D[team]


MATCHS = []


def SetUpDay():
    T = getmatchList()
    for id in T:
        m = match(id)
        MATCHS.append(m)
        TweetText("Match à venir: " + m.Tag)

SetUpDay()

schedule.every().day.at("10:30").do(SetUpDay)

while True:
    schedule.run_pending()
    time.sleep(1)

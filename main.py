from schedule import *
import schedule
import time

print("Importing....")

from twitt import *
from GetDatas import *

print("import done!")


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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
        up = getMatchUpdate()
        self.ScorerDom = ScorerParse(up["HomeGoalDetails"])
        self.ScorerAway = ScorerParse(up["AwayGoalDetails"])
        self.RedCardDom = ScorerParse(up["HomeTeamRedCardDetails"])
        self.RedCardAway = ScorerParse(up["AwayTeamRedCardDetails"])
        self.LineupHome = ""
        self.LineupAway = ""
        self.Status = up["Time"]
        schedule.every().day.at(timeop(self.Hour, 0, -30, 0)).do(self.getLU).tag(self.Tag)
        schedule.every().day.at(timeop(self.Hour, 0, -5, 0)).do(self.PrepareForMatch).tag(self.Tag)

    def PrepareForMatch(self):
        MATCHSDUJOUR.remove(self)
        MATCHSENCOURS.append(self)

    def score(self):
        return str(len(self.ScorerDom)) + "-" + str(len(self.ScorerAway))

    def actualisation(self, MU):
        stat = self.Status
        if stat == "FMT" or stat == "SMT":
            self.match_update(ScorerParse(MU["HomeGoalDetails"]), ScorerParse(MU["AwayGoalDetails"]),
                              ScorerParse(MU["HomeTeamRedCardDetails"]), ScorerParse(MU["AwayTeamRedCardDetails"]))
            self.time_update(MU["Time"])
        else:
            self.time_update(MU["Time"])
            self.match_update(ScorerParse(MU["HomeGoalDetails"]), ScorerParse(MU["AwayGoalDetails"]),
                              ScorerParse(MU["HomeTeamRedCardDetails"]), ScorerParse(MU["AwayTeamRedCardDetails"]))

    def time_update(self, stat):
        if self.Status != stat:
            if stat == "Match Finished":
                TweetFin(self.Dom, self.Away, self.Tag, self.score())
                schedule.clear(self.Tag)
                del self
            if stat == "Halftime":
                TweetMT(self.Dom, self.Away, self.Tag, self.score())
            if RepresentsInt(stat) and not RepresentsInt(self.Status):
                if int(stat) < 40:
                    TweetStart(self.Dom, self.Away, self.Tag)
                else:
                    TweetRep(self.Dom, self.Away, self.Tag, self.score())
            self.Status = stat

    def match_update(self, ScorD, ScorA, RCD, RCA):
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
        TweetText("Les compos de " + self.Tag + " sont sorties!")


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
        "Marseille": "OM",
        "Paris SG": "PSG",
        "St Etienne": "ASSE",
        "Angers": "SCO",
        "Monaco": "ASM",
        "Montpellier": "MHSC",
        "Lens": "RCL",
        "Lille": "LOSC",
        "Bordeaux": "FCGB",
        "Brest": "SB29",
        "Lorient": "FCL",
        "Nimes": "NO",
        "Strasbourg": "RCSA",
        "Metz": "FCM",
        "Nice": "OGCN",
        "Rennes": "SRFC",
        "Nantes": "FCN",
        "Dijon": "DFCO"
    }
    return D[team]


MATCHSDUJOUR = []
MATCHSENCOURS = []


def SetUpDay():
    T = getmatchList()
    for id in T:
        m = match(id)
        MATCHSDUJOUR.append(m)
        TweetText("Match à venir: " + m.Tag)


SetUpDay()

schedule.every().day.at("10:30").do(SetUpDay)


def getmatch(L, n):
    for m in L:
        if m["HomeTeam"] == n:
            return m


def UpdateMatches():
    if len(MATCHSENCOURS) == 0:
        return
    Matches_Updates = getMatchUpdate()
    for m in MATCHSENCOURS:
        m.actualisation(getmatch(Matches_Updates, m.Dom))


while True:
    schedule.run_pending()
    time.sleep(1)

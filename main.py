from schedule import *
import schedule
import time
from datetime import datetime

print("Importing....")

from twitt import *
from GetDatas import *

print("import done!")


def getmatch(L, n):
    for m in L:
        if m["HomeTeam"] == n:
            return m


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def islaterthan(t1, t2):
    h1, m1, s1 = int(t1[0:2]), int(t1[3:5]), int(t1[6:8])
    h2, m2, s2 = int(t2[0:2]), int(t2[3:5]), int(t2[6:8])
    if h1 > h2:
        return True
    if h1 < h2:
        return False
    if m1 > m2:
        return True
    if m1 < m2:
        return False
    if s1 < s2:
        return False
    return True


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
        up = getmatch(getMatchUpdate(), self.Dom)
        if up == None:
            self.ScorerDom = []
            self.ScorerAway = []
            self.RedCardDom = []
            self.RedCardAway = []
            self.Status = "Not Started"
            self.LineupHome = ""
            self.LineupAway = ""
        else:
            self.ScorerDom = ScorerParse(up.get("HomeGoalDetails", []))
            self.ScorerAway = ScorerParse(up.get("AwayGoalDetails", []))
            self.RedCardDom = ScorerParse(up.get("HomeTeamRedCardDetails", []))
            self.RedCardAway = ScorerParse(up.get("AwayTeamRedCardDetails", []))
            self.Status = up.get("Time", "Not Started")
            self.LineupHome = up.get("HomeLineupGoalkeeper", "") + "\n\n" + up.get("HomeLineupDefense",
                                                                                   "") + "\n\n" + up.get(
                "HomeLineupMidfield", "") + "\n\n" + up.get("HomeLineupForward", "")
            self.LineupAway = up.get("AwayLineupGoalkeeper", "") + "\n\n" + up.get("AwayLineupDefense",
                                                                                   "") + "\n\n" + up.get(
                "AwayLineupMidfield", "") + "\n\n" + up.get("AwayLineupForward", "")
        if islaterthan(datetime.now().strftime("%H:%M:%S"), timeop(self.Hour, 0, -30, 0)):
            self.getLU()
        else:
            schedule.every().day.at(timeop(self.Hour, 0, 30, 0)).do(self.getLU).tag(self.Tag)
        if islaterthan(datetime.now().strftime("%H:%M:%S"), timeop(self.Hour, 0, -5, 0)):
            self.PrepareForMatch()
        else:
            schedule.every().day.at(timeop(self.Hour, 0, 55, 0)).do(self.PrepareForMatch).tag(self.Tag)

    def PrepareForMatch(self):
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
            if stat.lower() == "match finished":
                TweetFin(self.Dom, self.Away, self.Tag, self.score())
                schedule.clear(self.Tag)
                del self
            if stat.lower() == "halftime":
                TweetMT(self.Dom, self.Away, self.Tag, self.score())
            if RepresentsInt(stat[:-1]) and (not RepresentsInt(self.Status)):
                if int(stat) < 40:
                    TweetStart(self.Dom, self.Away, self.Tag)
                else:
                    TweetRep(self.Dom, self.Away, self.Tag, self.score())
            self.Status = stat[:-1]

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
        up = getmatch(getMatchUpdate(), self.Dom)
        self.LineupHome = up["HomeLineupGoalkeeper"] + "\n" + up["HomeLineupDefense"] + "\n" + up[
            "HomeLineupMidfield"] + "\n" + up["HomeLineupForward"]
        self.LineupAway = up["AwayLineupGoalkeeper"] + "\n" + up["AwayLineupDefense"] + "\n" + up[
            "AwayLineupMidfield"] + "\n" + up["AwayLineupForward"]
        TweetLU(
            "La compo de #" + self.DomTag + ":\n\n" + self.LineupHome + "\n\n" + self.Tag, self.DomTag)
        TweetLU(
            "La compo de #" + self.AwayTag + ":\n\n" + self.LineupAway + "\n\n" + self.Tag, self.AwayTag)
        return


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
        TweetAnnonce("Match à venir: " + m.Tag, m.DomTag, m.AwayTag)


SetUpDay()

schedule.every().day.at("10:30").do(SetUpDay)


def UpdateMatches():
    if len(MATCHSENCOURS) == 0:
        return
    Matches_Updates = getMatchUpdate()
    for m in MATCHSENCOURS:
        m.actualisation(getmatch(Matches_Updates, m.Dom))


while True:
    schedule.run_pending()
    UpdateMatches()
    time.sleep(1)

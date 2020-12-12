import os
from datetime import date

import requests
import json

LIGUEID = 4334
LIGUENAME = "Ligue 1"
KEY = os.environ["KEY"]
print(KEY)


"""
reponse = requests.get(" https://www.thesportsdb.com/api/v1/json/"+KEY+"/eventsnextleague.php?id= "+ LIGUEID)

print(reponse.content)
"""
"""
reponse = requests.get("https://www.thesportsdb.com/api/v1/json/1/lookupevent.php?id=1031304")

print(reponse.content)
"""
"""
reponse = requests.get(" https://www.thesportsdb.com/api/v1/json/1/lookupeventstats.php?id=1031304")

print(reponse.content)
"""


def epuration(str):
    for i in range(len(str)):
        if str[i] == "[":
            return str[i + 1: -2]


def parse_in_dictionary(str):
    T = []
    i = 0
    while 0 == 0:
        D = dict()
        while str[i] != "}":
            deb = i
            while str[i] != ":":
                i += 1
            sep = i
            while str[i] != "," and str[i] != "}":
                i += 1
            key = str[deb + 2:sep - 1]
            val = str[sep + 1:i]
            if val[0] == "\"":
                val = val[1:-1]
            else:
                val = None
            D[key] = val
        T.append(D)
        i += 1
        if i >= len(str) or str[i] == "]":
            return T
        i += 1


def getResponseInDict(req):
    reponse = requests.get(req).content.decode(
        "UTF-8")
    reponse2 = json.loads(reponse)
    """
    reponse = epuration(reponse)
    reponse = parse_in_dictionary(reponse)
    """


    return reponse2


def getMatchsInfos(id):
    reponse = getResponseInDict("https://www.thesportsdb.com/api/v1/json/"+str(KEY)+"/lookupevent.php?id=" + str(id))["events"][0]
    return reponse["strHomeTeam"], reponse["strAwayTeam"], reponse["strTime"]


def getMatchUpdate():
    reponse = getResponseInDict("https://www.thesportsdb.com/api/v1/json/"+str(KEY)+"/latestsoccer.php")["teams"]["Match"]
    toreturn = []
    for r in reponse:
        if r["League"] == LIGUENAME:
            toreturn.append(r)
    return toreturn


def getmatchList():
    reponse = getResponseInDict(" https://www.thesportsdb.com/api/v1/json/"+str(KEY)+"/eventsnextleague.php?id="+str(LIGUEID))["events"]
    today = date.today().strftime("%Y-%m-%d")
    RET = []
    for m in reponse:
        if m["dateEvent"] == today:
            RET.append(m["idEvent"])
    return RET


def ScorerParse(sc):
    if sc==None:
        return []
    T = []
    i = 0
    while i < len(sc):
        D = []
        deb = i
        while sc[i] != ":":
            i += 1
        sep = i
        while sc[i] != ";":
            i += 1
        min = sc[deb:sep]
        but = sc[sep + 1:i]
        D.append(min)
        D.append(but)
        T.append(D)
        i += 1
    return T

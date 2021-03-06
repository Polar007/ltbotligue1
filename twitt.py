from os import path
import os

import tweepy

APIKey = os.environ["APIKey"]
APISecret = os.environ["APISecret"]

ACCESToken = os.environ["ACCESSToken"]
ACCESTokenSecret = os.environ["ACCESSTokenSecret"]

auth = tweepy.OAuthHandler(APIKey, APISecret)
auth.set_access_token(ACCESToken, ACCESTokenSecret)

api = tweepy.API(auth)


def SearchGif(TeamTag):
    name = "GIFs/Gif " + TeamTag + ".gif"
    if path.exists(name):
        return "GIFs/Gif " + TeamTag + ".gif"
    return "NOTEX"


def SearchLogo(TeamTag):
    name = "COMPOS/" + TeamTag + ".png"
    if path.exists(name):
        return "COMPOS/" + TeamTag + ".png"
    return "NOTEX"


def SearchRedCard(TeamTag):
    name = "CartonsRouges/" + TeamTag + ".jpg"
    if path.exists(name):
        return "CartonsRouges/" + TeamTag + ".jpg"
    return "NOTEX"


def TweetText(text):
    try:
        api.update_status(text)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            # Do nothing
            print('duplicate message')
        else:
            raise error


def TweetMedia(text, media):
    try:
        media_ids = []
        for filename in media:
            res = api.media_upload(filename)
            media_ids.append(res.media_id)
        api.update_status(status=text, media_ids=media_ids)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            # Do nothing
            print('duplicate message')
        else:
            raise error


def TweetStart(Dom, Away, Tag):
    TweetText("1': Coup d'envoi du match entre " + Dom + " et " + Away + "!\n\n" + Tag + " (0-0)")


def TweetMT(Dom, Away, Tag, Score):
    TweetText("Mi Temps entre " + Dom + " et " + Away + "!\n\n" + Tag + " (" + Score + ")")


def TweetRep(Dom, Away, Tag, Score):
    TweetText("46': c'est repartie entre " + Dom + " et " + Away + "!\n\n" + Tag + " (" + Score + ")")


def TweetFin(Dom, Away, Tag, Score):
    TweetText("C'est terminé entre " + Dom + " et " + Away + "!\n\n" + Tag + " (" + Score + ")")


def TweetGoal(TeamTag, Scorer, Min, Tag, Score):
    Gif = SearchGif(TeamTag)
    if Gif == "NOTEX":
        TweetText(Min + "': BUUUUUUUUUUUUUT  #" + TeamTag + " de " + Scorer + "!\n\n" + Tag + " (" + Score + ")")
    else:
        TweetMedia(Min + "': BUUUUUUUUUUUUUT pour #" + TeamTag + " de " + Scorer + "!\n\n" + Tag + " (" + Score + ")",
                   [Gif])


def TweetRedCard(TeamTag, Player, Min, Tag, Score):
    Gif = SearchRedCard(TeamTag)
    if Gif == "NOTEX":
        TweetText(
            Min + "': CARTON ROUGE POUR #" + TeamTag + "! " + Player + "est expulsé!\n\n" + Tag + " (" + Score + ")")
    else:
        TweetMedia(Min + "': CARTON ROUGE POUR #" + Player + "!\n\n" + Tag + " (" + Score + ")", [Gif])


def TweetAnnonce(text, Dom, Ext):
    GifD = SearchLogo(Dom)
    GifE = SearchLogo(Ext)
    if GifE == "NOTEX" or GifD == "NOTEX":
        TweetText(text)
    else:
        TweetMedia(text, [GifD, GifE])


def TweetLU(text, Tag):
    Gif = SearchLogo(Tag)
    if Gif == "NOTEX":
        TweetText(text)
    else:
        TweetMedia(text, [Gif])

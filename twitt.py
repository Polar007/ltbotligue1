from os import path

import tweepy

APIKey = "SNe7BdvnmuMtARbbN4EabPJI6"
APISecret = "60dIEdrcl5OVzxy7kvVmlisGaqEqeqICtCTDZfI5u4OFzvGS1J"

ACCESToken = "1424013613-IZhfoFkn4kWr64oS954YD8R9EM4aSpEHQdJWWJD"
ACCESTokenSecret = "2CqpfBPPfSXrriIGKNTWGmnLWlO7GCNDnAmNyZ8HCMvfw"

auth = tweepy.OAuthHandler(APIKey, APISecret)
auth.set_access_token(ACCESToken, ACCESTokenSecret)

api = tweepy.API(auth)


def SearchGif(TeamTag):
    name = "GIFs/Gif " + TeamTag + ".gif"
    if path.exists(name):
        return "GIFs/Gif " + TeamTag + ".gif"
    return "NOTEX"


def SearchRedCard(TeamTag):
    return ""


def TweetText(text):
    api.update_status(text)


def TweetMedia(text, media):
    api.update_with_media(media, text)


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
        TweetText(Min + "': BUUUUUUUUUUUUUT pour" + TeamTag + " de " + Scorer + "!\n\n" + Tag + " (" + Score + ")")
    TweetMedia(Min + "': BUUUUUUUUUUUUUT pour" + TeamTag + " de " + Scorer + "!\n\n" + Tag + " (" + Score + ")", Gif)


def TweetRedCard(TeamTag, Player, Min, Tag, Score):
    Gif = SearchRedCard(TeamTag)
    if Gif == "NOTEX":
        TweetText(Min + "': CARTON ROUGE POUR " + TeamTag + "! " + Player + "est expulsé!\n\n" + Tag + " (" + Score + ")", SearchRedCard(TeamTag))
    TweetMedia(Min + "': CARTON ROUGE POUR " + Player + "!\n\n" + Tag + " (" + Score + ")", SearchRedCard(TeamTag))

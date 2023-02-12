import json
import os
import webbrowser
import configparser
from os.path import join, dirname

import instaloader as IL
from dotenv import load_dotenv
from instaloader import instaloader

outDir = 'out'
directory = outDir + '/whoIsNotFollowingBack.txt'
instagramLink = 'https://www.instagram.com/'


def parseJson(file):
    items = []
    with open(file) as f:
        data = json.load(f)
        typeRelationShips = 'relationships_following' if 'relationships_following' in data else 'relationships_followers'

        for i in data[typeRelationShips]:
            for j in i['string_list_data']:
                item = j['value'] + ' (' + j['href'] + ')'
                items.append(item)
    return sortList(items)


def sortList(list):
    return sorted(list)


def createOutFolder():
    if not os.path.exists(outDir):
        os.makedirs(outDir)


def createOutFile():
    createOutFolder()
    if not os.path.exists(directory):
        with open(directory, 'w') as f:
            f.write('')
    else:
        os.remove(directory)
        createOutFile()
    return


def createHTMLFile():
    file_html = open(f"{outDir}/whoIsNotFollowingBack.html", "w")
    file_html.write('''<html>
    <head>
    <title>Instollowing</title>
    </head> 
    <body>
    <h1>That's who is not following you back</h1>     
    <ul>
    ''')
    with open(directory, 'r') as f:
        for line in f:
            url = line.split(' ')[1].replace('(', '').replace(')', '')
            line = '<a href="' + url + '">' + line.split(' ')[0] + '</a>'

            file_html.write('<li>' + line + '</li>')
    file_html.write('''</ul>
    </body>
    </html>''')
    file_html.close()
    url = 'file://' + os.path.realpath(file_html.name)
    webbrowser.open(url, new=2)  # open in new tab


def loginInstagram():
    dotenv_path = join(dirname(__file__), '.env')

    load_dotenv(dotenv_path)

    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")

    il = IL.Instaloader()
    il.login(username, password)

    return il


def getFollowersAndFollowing(usernameToCheck):
    il = loginInstagram()
    profile = instaloader.Profile.from_username(il.context, usernameToCheck)

    followers_list, following_list = list(profile.get_followers()), list(profile.get_followees())
    followers, following = [], []

    for follower in followers_list:
        followers.append(follower.username + ' (' + instagramLink + follower.username + ')')

    for followee in following_list:
        following.append(followee.username + ' (' + instagramLink + followee.username + ')')

    followers = sorted(followers)
    following = sorted(following)

    return following, followers


def whoIsNotFollowingBack(following, followers):
    createOutFile()
    for user in following:
        if user not in followers:
            with open(directory, 'a') as f:
                f.write(user + '\n')

    createHTMLFile()

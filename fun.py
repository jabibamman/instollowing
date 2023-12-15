import csv
import json
import os
import webbrowser
import instaloader as IL
from instaloader import instaloader

outDir = 'out'
directory = outDir + '/whoIsNotFollowingBack.csv'
instagramLink = 'https://www.instagram.com/'
imgUrl = "logo.jpg"


def parseJson(file):
    items = list()
    with open(file) as f:
        data = json.load(f)
        typeRelationShips = 'relationships_following' if 'relationships_following' in data else 'relationships_follower'

        for i in data[typeRelationShips]:
            for j in i['string_list_data']:
                item = {
                    'username': j['value'],
                    'url': j['href'],
                    'imgUrl': imgUrl
                }
                items.append(item)
    return sortList(items)


def sortList(items):
    return sorted(items, key=lambda x: x['username'])


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
    with open(directory, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0] == 'username': continue

            line = ('<img src="' + row[2] + '" width="50" height="50">') + (
                    '<a href="' + row[1] + '">' + row[0] + '</a>') if row[2] != 'none' else (
                    '<a href="' + row[1] + '">' + row[0] + '</a>')

            file_html.write('<li>' + line + '</li>')
            file_html.write('\n     ')
    file_html.write('''
    </ul>
  </body>
</html>
''')
    file_html.close()
    url = 'file://' + os.path.realpath(file_html.name)
    webbrowser.open(url, new=2)


# Actually this function is not fully working because of the 2FA
def loginInstagram():
    with open('credentials.json') as f:
        credentials = json.load(f)

    username = credentials['username']
    password = credentials['password']

    il = IL.Instaloader()

    try:
        il.login(username, password)
        print("Successfully logged in.")
    except instaloader.TwoFactorAuthRequiredException:
        code_2fa = input("2FA Code : ")
        il.two_factor_login(code_2fa)

    return il


def getFollowersAndFollowing():
    usernameToCheck = "abib_james"
    il = loginInstagram()
    profile = instaloader.Profile.from_username(il.context, usernameToCheck)

    followers_list, following_list = list(profile.get_followers()), list(profile.get_followees())
    followers, following = [], []

    for follower in followers_list:
        followers.append(follower.username + ";" + instagramLink + follower.username + ";none")

    for followee in following_list:
        following.append(followee.username + ';' + instagramLink + followee.username)

    followers = sorted(followers)
    following = sorted(following)

    return following, followers


def whoIsNotFollowingBack(following, followers):
    createOutFile()
    usernames_followers = {f['username'] for f in followers}

    for user in following:
        print(user)
        if user['username'] not in usernames_followers:
            with open(directory, 'a') as f:
                if os.stat(directory).st_size == 0:
                    f.write('username;url;imgUrl\n')

                user_info = f"{user['username']};{user['url']};{user['imgUrl']}"
                f.write(user_info + '\n')

    createHTMLFile()

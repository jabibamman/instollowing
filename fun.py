import csv
import json
import os
import webbrowser
import instaloader as IL
from instaloader import instaloader


class Instollowing:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        if self.username is not None or self.password is not None:
            self.ig = IL.Instaloader()
            self.ig.login(username, password)
        self.outDir = "out"
        self.directory = self.outDir + "/whoIsNotFollowingBack.csv"
        self.instagramLink = "https://www.instagram.com/"
        self.imgUrl = "logo.jpg"

    def parseJson(self, file):
        items = list()
        with open(file) as f:
            data = json.load(f)
            typeRelationShips = (
                "relationships_following"
                if "relationships_following" in data
                else "relationships_follower"
            )

            for i in data[typeRelationShips]:
                for j in i["string_list_data"]:
                    item = {
                        "username": j["value"],
                        "url": j["href"],
                        "imgUrl": self.imgUrl,
                    }
                    items.append(item)
        return self.sortList(items)

    def sortList(self, items):
        return sorted(items, key=lambda x: x["username"])

    def createOutFolder(self):
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)

    def createCSVFile(self):
        self.createOutFolder()
        if not os.path.exists(self.directory):
            with open(self.directory, "w") as f:
                f.write("")
        else:
            os.remove(self.directory)
            self.createCSVFile()
        return

    def createHTMLFile(self):
        file_html = open(f"{self.outDir}/whoIsNotFollowingBack.html", "w")
        file_html.write(
            """<html>
        <head>
        <title>Instollowing</title>
        </head> 
        <body>
        <h1>That's who is not following you back</h1>     
        <ul>
        """
        )
        with open(self.directory, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            for row in reader:
                if row[0] == "username":
                    continue

                line = (
                    ('<img src="' + row[2] + '" width="50" height="50">')
                    + ('<a href="' + row[1] + '">' + row[0] + "</a>")
                    if row[2] != "none"
                    else ('<a href="' + row[1] + '">' + row[0] + "</a>")
                )

                file_html.write("<li>" + line + "</li>")
                file_html.write("\n     ")
        file_html.write(
            """
        </ul>
      </body>
    </html>
    """
        )
        file_html.close()
        url = "file://" + os.path.realpath(file_html.name)
        webbrowser.open(url, new=2)

    def getFollowersAndFollowing(self):
        profile = instaloader.Profile.from_username(self.ig.context, self.username)

        followers_list, following_list = list(profile.get_followers()), list(
            profile.get_followees()
        )
        followers, following = [], []

        for follower in followers_list:
            followers.append(
                follower.username
                + ";"
                + self.instagramLink
                + follower.username
                + ";none"
            )

        for followee in following_list:
            following.append(
                followee.username + ";" + self.instagramLink + followee.username
            )

        followers = sorted(followers)
        following = sorted(following)

        return following, followers

    def whoIsNotFollowingBack(self, following, followers):
        self.createCSVFile()
        usernames_followers = {f["username"] for f in followers}

        for user in following:
            if user["username"] not in usernames_followers:
                with open(self.directory, "a") as f:
                    user_info = f"{user['username']};{user['url']};{user['imgUrl']}"
                    f.write(user_info + "\n")

        self.createHTMLFile()

    def run(self):
        if self.username is None or self.password is None:
            following, followers = self.parseJson("following.json"), self.parseJson(
                "followers.json"
            )
        else:
            following, followers = self.getFollowersAndFollowing()

        self.whoIsNotFollowingBack(following, followers)

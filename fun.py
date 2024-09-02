import csv
import json
import os
import webbrowser
from datetime import datetime
import logging
import instaloader as IL
from instaloader import instaloader
from pathlib import Path

log_dir = Path("out/log")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="w"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("InstollowingLogger")


class Instollowing:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        if self.username is not None or self.password is not None:
            self.ig = IL.Instaloader()
            self.ig.login(username, password)
        self.outDir = Path("out")
        self.oldDir = self.outDir / "old"
        self.followingsPath = Path("following.json")
        self.followersPath = Path("followers.json")
        self.followingPath = Path("following.json")
        self.directory = self.outDir / "whoIsNotFollowingBack.csv"
        self.instagramLink = "https://www.instagram.com/"
        self.imgUrl = "logo.jpg"
        logger.info("Instollowing initialized")

    def parseJson(self, file):
        logger.info(f"Parsing JSON file: {file}")
        items = list()

        try:
            with open(file) as f:
                data = json.load(f)
                if "relationships_following" in data:
                    data_to_iterate = data["relationships_following"]
                elif "relationships_follower" in data:
                    data_to_iterate = data["relationships_follower"]
                else:
                    data_to_iterate = data

                for relationship_data in data_to_iterate:
                    for j in relationship_data.get("string_list_data", []):
                        item = {
                            "username": j["value"],
                            "url": j["href"],
                            "imgUrl": self.imgUrl,
                        }
                        items.append(item)

        except FileNotFoundError as e:
            logger.error(f"File not found: {file}. Exception: {e}")
            raise

        return self.sortList(items)

    @staticmethod
    def sortList(items):
        return sorted(items, key=lambda x: x["username"])

    def createOutFolder(self):
        if not self.outDir.exists():
            self.outDir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output directory created: {self.outDir}")

    def createCSVFile(self):
        self.createOutFolder()
        if self.directory.exists():
            self.directory.unlink()

            logger.info(f"Old CSV file deleted: {self.directory}")

        with self.directory.open('w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["username", "url", "imgUrl"])  # Adding header row
            logger.info(f"CSV file created: {self.directory}")

    def createHTMLFile(self):
        logger.info(f"Creating HTML file from: {self.directory}")
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
        logger.info(f"HTML file created and opened in browser: {url}")

    def getFollowersAndFollowing(self):
        try:
            logger.info(f"Retrieving followers and following for user: {self.username}")
            profile = instaloader.Profile.from_username(self.ig.context, self.username)

            followers = sorted([
                f"{follower.username};{self.instagramLink}{follower.username};none"
                for follower in profile.get_followers()
            ])

            following = sorted([
                f"{followee.username};{self.instagramLink}{followee.username};none"
                for followee in profile.get_followees()
            ])

        except IL.ProfileNotExistsException as e:
            logger.error(f"Profile not found: {self.username}. Exception: {e}")
            raise

        return following, followers

    def whoIsNotFollowingBack(self, following, followers):
        self.createCSVFile()
        usernames_followers = {f["username"] for f in followers}

        with self.directory.open('a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            for user in following:
                if user["username"] not in usernames_followers:
                    writer.writerow([user['username'], user['url'], user['imgUrl']])

        logger.info("Finished checking who is not following back")
        self.createHTMLFile()

    def archiveInput(self):
        self.createOutFolder()

        Path(self.followersPath).rename(self.oldDir / f"followers_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
        Path(self.followingPath).rename(self.oldDir / f"following_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
        logger.info("Old files archived")

    def run(self):
        logger.info("Instollowing run started")
        if self.username is None or self.password is None:
            following, followers = self.parseJson(self.followingPath), self.parseJson(
                self.followersPath
            )

            self.archiveInput()
        else:
            following, followers = self.getFollowersAndFollowing()

        self.whoIsNotFollowingBack(following, followers)
        logger.info("Instollowing run finished")

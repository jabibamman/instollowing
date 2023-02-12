from fun import *

if __name__ == '__main__':
    # si on a pas de fichier followers.json et following.json
    if not os.path.exists('followers.json') or not os.path.exists('following.json'):
        usernameToCheck = input("Enter the username to get people who are not following you back: ")

        # on récupère les followers et following de l'utilisateur choisi
        following, followers = getFollowersAndFollowing(usernameToCheck)
    else:
        # sinon on les parse
        following = parseJson('following.json')
        followers = parseJson('followers.json')

    whoIsNotFollowingBack(following, followers)


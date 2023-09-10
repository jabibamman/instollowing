from fun import *

if __name__ == '__main__':
    if not os.path.exists('followers.json') or not os.path.exists('following.json'):
        usernameToCheck = input("Enter the username to get people who are not following you back: ")
        following, followers = getFollowersAndFollowing(usernameToCheck)
    else:
        # sinon on les parse
        following = parseJson('following.json')
        followers = parseJson('followers.json')

    whoIsNotFollowingBack(following, followers)
    

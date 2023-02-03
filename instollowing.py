from fun import *

if __name__ == '__main__':
    following = parseJson('following.json')
    followers = parseJson('followers.json')

    whoIsNotFollowingBack(following, followers)


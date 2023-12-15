from fun import *

if __name__ == '__main__':
    if not os.path.exists('followers.json') or not os.path.exists('following.json'):
        following, followers = getFollowersAndFollowing()
    else:
        following = parseJson('following.json')
        followers = parseJson('followers.json')

    whoIsNotFollowingBack(following, followers)
    

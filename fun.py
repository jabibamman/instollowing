import json
import os

outDir = 'out'
directory = outDir + '/whoIsNotFollowingBack.txt'


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


def whoIsNotFollowingBack(list1, list2):
    createOutFile()
    for user in following:
        if user not in followers:
            with open(directory, 'a') as f:
                f.write(user + '\n')

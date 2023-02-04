import json
import os
import webbrowser

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
    webbrowser.open(url, new=2) # open in new tab


def whoIsNotFollowingBack(following, followers):
    createOutFile()
    for user in following:
        if user not in followers:
            with open(directory, 'a') as f:
                f.write(user + '\n')

    createHTMLFile()

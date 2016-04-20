import giphypop

g = giphypop.Giphy()


def getGiphy(tag):
    url = g.screensaver(tag=tag).original.url
    newUrl = url.split("/")[4]
    return "https://media.giphy.com/media/{0}/giphy.gif".format(newUrl)